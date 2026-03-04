use crate::{
    fetching_page::FetchingPageFuture, future_result::FutureResult, storing_db::StoringFuture,
};

pub enum State {
    FetchPage,
    StoringToDatabase,
    Done,
}

pub struct CrawlFuture {
    state: State,
    fetching_page_fut: FetchingPageFuture,
    storing_db_fut: StoringFuture,
    page: [u8; 16],
}

impl CrawlFuture {
    pub fn new() -> CrawlFuture {
        CrawlFuture {
            state: State::FetchPage,
            fetching_page_fut: FetchingPageFuture::new(),
            storing_db_fut: StoringFuture::new(),
            page: [0; 16],
        }
    }

    pub fn poll(&mut self) -> FutureResult<()> {
        match self.state {
            State::FetchPage => {
                println!("Fetching page...");
                match self.fetching_page_fut.poll(&mut self.page) {
                    FutureResult::Pending => FutureResult::Pending,
                    FutureResult::Ready(_) => {
                        self.state = State::StoringToDatabase;
                        FutureResult::Pending
                    }
                }
            }
            State::StoringToDatabase => {
                println!("Storing to database...");
                match self.storing_db_fut.poll(&self.page) {
                    FutureResult::Pending => FutureResult::Pending,
                    FutureResult::Ready(_) => {
                        self.state = State::Done;
                        FutureResult::Pending
                    }
                }
            }
            State::Done => {
                println!("Done!");
                FutureResult::Ready(())
            }
        }
    }
}

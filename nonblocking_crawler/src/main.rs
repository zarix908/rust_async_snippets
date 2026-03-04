use std::{thread, time::Duration};

use crate::{crawl::CrawlFuture, future_result::FutureResult};

mod crawl;
mod fetching_page;
mod future_result;
mod storing_db;

fn main() {
    let mut fetchers = Vec::new();
    for _ in 1..10000 {
        fetchers.push(CrawlFuture::new());
    }

    loop {
        let mut all_ready = true;

        for fetcher in &mut fetchers {
            match fetcher.poll() {
                FutureResult::Pending => all_ready = false,
                FutureResult::Ready(_) => (),
            }
        }

        if all_ready {
            break;
        }
        thread::sleep(Duration::from_millis(100));
    }
}

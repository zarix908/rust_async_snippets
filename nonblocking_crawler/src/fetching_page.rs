use std::{
    io::Write,
    ops::Add,
    time::{self, Duration},
};

use crate::future_result::FutureResult;

pub struct FetchingPageFuture {
    deadline: time::Instant,
}

impl FetchingPageFuture {
    pub fn new() -> FetchingPageFuture {
        FetchingPageFuture {
            deadline: time::Instant::now().add(Duration::from_secs(3)),
        }
    }

    pub fn poll(&mut self, mut page: &mut [u8]) -> FutureResult<()> {
        if time::Instant::now() < self.deadline {
            return FutureResult::Pending;
        }

        page.write(b"Hello, world").unwrap();
        FutureResult::Ready(())
    }
}

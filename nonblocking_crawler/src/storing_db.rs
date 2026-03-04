use std::{
    ops::Add,
    time::{self, Duration},
};

use crate::future_result::FutureResult;

pub struct StoringFuture {
    deadline: time::Instant,
}

impl StoringFuture {
    pub fn new() -> StoringFuture {
        StoringFuture {
            deadline: time::Instant::now().add(Duration::from_secs(6)),
        }
    }

    pub fn poll(&mut self, page: &[u8]) -> FutureResult<()> {
        if time::Instant::now() < self.deadline {
            return FutureResult::Pending;
        }

        println!(r"INSERT ( {} )", str::from_utf8(&page).unwrap());
        FutureResult::Ready(())
    }
}

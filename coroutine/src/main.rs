#![feature(coroutines, coroutine_trait, stmt_expr_attributes)]

use std::collections::HashSet;
use std::ops::{Add, Coroutine, CoroutineState};
use std::pin::Pin;
use std::time::{self, Duration};

fn main() {
    let fetch_deadline = time::Instant::now().add(Duration::from_secs(3));
    let store_deadline = time::Instant::now().add(Duration::from_secs(6));
    let mut coroutines = Vec::new();

    for i in 1..10000 {
        let coro = #[coroutine] || {
            loop {
                if time::Instant::now() >= fetch_deadline {
                    break;
                }

                yield "Fetching page..."
            }

            loop {
                if time::Instant::now() >= store_deadline {
                    break;
                }

                yield "Storing to database..."
            }

            return "Done!";
        };

        coroutines.push(coro);
    }

    let mut completed = HashSet::new();
    loop {
        for (i, coro) in coroutines.iter_mut().enumerate() {
            if completed.get(&i).is_some() {
                continue;
            }

            match Pin::new(coro).resume(()) {
                CoroutineState::Yielded(x) => {
                    println!("{}", x);
                }
                CoroutineState::Complete(x) => {
                    println!("{}", x);
                    completed.insert(i);
                }
            }
        }

        if completed.len() == coroutines.len() {
            break;
        }
    }
}

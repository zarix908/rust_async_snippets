#![feature(coroutines, coroutine_trait, stmt_expr_attributes)]

use std::ops::{Coroutine, CoroutineState};
use std::pin::Pin;

fn main() {
    let mut coroutine = #[coroutine] || {
        yield 1;
        yield 25;
        return "foo"
    };

    loop {
        match Pin::new(&mut coroutine).resume(()) {
            CoroutineState::Yielded(x) => println!("{}", x),
            CoroutineState::Complete(x) => {
                println!("{}", x);
                break;
            },
        }
    }
}

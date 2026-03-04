use std::{mem, pin::pin};

use crate::selfref::SelfRef;

mod selfref;

fn main() {
    let mut s1 = pin!(SelfRef::new("value1"));
    let mut s2 = pin!(SelfRef::new("value2"));
    s1.as_mut().init();
    s2.as_mut().init();

    println!("=================================================");
    println!(
        "value: {}, value by ptr: {}",
        s1.as_ref().value(),
        s1.value_by_ptr()
    );

    mem::swap(s1.as_mut().get_mut(), s2.as_mut().get_mut());
    println!("========================swap=====================");

    println!("value: {}, value by ptr: {}", s2.value(), s2.value_by_ptr());
    println!("=================================================");
}

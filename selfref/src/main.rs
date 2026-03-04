use std::mem;

use crate::selfref::SelfRef;

mod selfref;

fn main() {
    let mut s1 = SelfRef::new("value1");
    let mut s2 = SelfRef::new("value2");
    s1.init();
    s2.init();

    println!("=================================================");
    println!("value: {}, value by ptr: {}", s1.value(), s1.value_by_ptr());

    mem::swap(&mut s1, &mut s2);
    println!("========================swap=====================");

    println!("value: {}, value by ptr: {}", s2.value(), s2.value_by_ptr());
    println!("=================================================");
}

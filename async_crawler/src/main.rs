use std::{io::Write, time::Duration};

use tokio::time;

#[tokio::main]
async fn main() {
    println!("Fetching page...");
    
    let mut page = [0u8; 16];
    (async |mut page: &mut [u8]| {
        time::sleep(Duration::from_secs(5)).await;
        page.write(b"Hello, world").unwrap();
    })(&mut page).await;

    println!("Storing to database...");
    
    time::sleep(Duration::from_secs(3)).await;
    println!("");
    
    println!("Done!");
}

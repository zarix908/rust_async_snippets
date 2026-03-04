use std::{io::Write, time::Duration};

use futures::future;
use tokio::time;

#[tokio::main]
async fn main() {
    let mut fetchers = Vec::new();
    for _ in 1..10000 {
        fetchers.push(crawl());
    }

    future::join_all(fetchers).await;
}

async fn crawl() {
    println!("Fetching page...");

    let mut page = [0u8; 16];
    (async |mut page: &mut [u8]| {
        time::sleep(Duration::from_secs(3)).await;
        page.write(b"Hello, world").unwrap();
    })(&mut page)
    .await;

    println!("Storing to database...");

    time::sleep(Duration::from_secs(3)).await;
    println!(r"INSERT ( {} )", str::from_utf8(&page).unwrap());

    println!("Done!");
}

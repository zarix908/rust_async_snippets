use std::time::Duration;

use tokio::time::sleep;

#[tokio::main]
async fn main() {
    let dur = Duration::from_secs(1);
    sleep(dur).await;
}

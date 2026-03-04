pub enum FutureResult<T> {
    Pending,
    Ready(T),
}

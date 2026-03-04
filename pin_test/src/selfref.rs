use std::pin::Pin;

pub struct SelfRef {
    value: String,
    value_ptr: *const String,
}

impl SelfRef {
    pub fn new(value: &str) -> Self {
        SelfRef {
            value: String::from(value),
            value_ptr: std::ptr::null(),
        }
    }

    pub fn init(self: Pin<&mut Self>) {
        let value_ptr: *const String = &self.value;

        // SAFETY: the data will never move out of this reference in this function
        let this = unsafe { self.get_unchecked_mut() };
        this.value_ptr = value_ptr;
    }

    pub fn value(&self) -> &str {
        &self.value
    }

    pub fn value_by_ptr(&self) -> &str {
        assert!(
            !self.value_ptr.is_null(),
            "SelfRef called without being set_ptr called first"
        );
        unsafe { &*(self.value_ptr) }
    }
}

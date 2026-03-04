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

    pub fn init(&mut self) {
        let value_ptr: *const String = &self.value;
        self.value_ptr = value_ptr;
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

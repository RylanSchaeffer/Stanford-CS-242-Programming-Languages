extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

// Copy of the provided cart_invalid_method1 test
fn main() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            // `checkout` method should be inaccessible in empty state.
            empty.checkout();
        }
    }
}

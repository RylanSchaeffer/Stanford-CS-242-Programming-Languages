extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

fn main() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let _nonempty = empty.add_item(1);
            // `empty` object should not be used again.
            empty.add_item(1);
        }
    }
}

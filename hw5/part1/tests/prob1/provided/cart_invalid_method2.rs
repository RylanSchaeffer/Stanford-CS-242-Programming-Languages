extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

fn main() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let checkout = nonempty.checkout();
            let nonempty = checkout.cancel();
            // `order` method should be inaccessible in nonempty state.
            nonempty.order();
        }
    }
}

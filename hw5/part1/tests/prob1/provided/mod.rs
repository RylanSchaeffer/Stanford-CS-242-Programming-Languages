extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

/**************
 * Test Cases *
 **************/
#[test]
fn valid_01_login_err() {
    match Cart::login("id99".to_string(), "pw99".to_string()) {
        Err(()) =>
            (),
        Ok(_empty) =>
            assert!(false), // `login` should fail.
    }
}

#[test]
fn valid_02_login_ok() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false), // `login` should succeed.
        Ok(empty) => {
            assert_eq!(empty.acct_num(), 123); // `acct_num` should be 123.
            assert_eq!(empty.tot_cost(), 0);   // `tot_cost` should be 0.
        }
    }
}

#[test]
fn valid_03_add_item_once() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            assert_eq!(nonempty.acct_num(), 123);
            assert_eq!(nonempty.tot_cost(), 1);   // `tot_cost` should be 1.
        }
    }
}

#[test]
fn valid_04_add_item_twice() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let nonempty = nonempty.add_item(2);
            assert_eq!(nonempty.acct_num(), 123);
            assert_eq!(nonempty.tot_cost(), 3); // `tot_cost` should be 3.
        }
    }
}

#[test]
fn valid_05_checkout() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) => assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let nonempty = nonempty.add_item(2);
            let checkout = nonempty.checkout();
            assert_eq!(checkout.acct_num(), 123);
            assert_eq!(checkout.tot_cost(), 3); // `tot_cost` should be 3.
        }
    }
}

#[test]
fn valid_06_cancel() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) => assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let nonempty = nonempty.add_item(2);
            let checkout = nonempty.checkout();
            let nonempty = checkout.cancel();
            assert_eq!(nonempty.acct_num(), 123);
            assert_eq!(nonempty.tot_cost(), 3); // `tot_cost` should be 3.
        }
    }
}

#[test]
fn valid_07_clear_items() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) => assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let nonempty = nonempty.add_item(2);
            let checkout = nonempty.checkout();
            let nonempty = checkout.cancel();
            let empty    = nonempty.clear_items();
            assert_eq!(empty.acct_num(), 123);
            assert_eq!(empty.tot_cost(), 0); // `tot_cost` should be 0.
        }
    }
}

#[test]
fn valid_08_order() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let nonempty = empty.add_item(1);
            let nonempty = nonempty.add_item(2);
            let checkout = nonempty.checkout();
            let empty    = checkout.order();
            assert_eq!(empty.acct_num(), 123);
            assert_eq!(empty.tot_cost(), 0); // `tot_cost` should be 0.
        }
    }
}

#[test]
fn invalid() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/prob1/provided/cart_invalid_*.rs"); // compile should fail for these files.
}

extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

// Use this file to write your own custom tests.
// Valid tests:
// - Write new valid tests below by naming your function valid_* and including
//   #[test] above each test.
//
// Invalid tests:
// - You can add new invalid tests by creating new test files in the same directory
//   and naming the files cart_invalid_*.rs.
// - Each invalid test needs to include a main function with invalid uses of the Cart API.
//   Feel free to use the provided cart_invalid_*.rs test files as templates (i.e. copy paste) for
//   the file structure and import statements.

// This test is a copy of the provided valid_01_login_err test.
#[test]
fn valid_test_example() {
    match Cart::login("id99".to_string(), "pw99".to_string()) {
        Err(()) =>
            (),
        Ok(_empty) =>
            assert!(false), // `login` should fail.
    }
}

// DO NOT MODIFY. This test case ensures that all the invalid tests don't compile.
#[test]
fn invalid() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/prob1/custom/cart_invalid_*.rs");
}
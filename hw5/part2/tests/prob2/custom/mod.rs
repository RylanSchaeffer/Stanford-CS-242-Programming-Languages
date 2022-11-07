extern crate part2;
#[allow(unused_imports)]
use part2::prob2::msg::Pkt;
#[allow(unused_imports)]
use part2::prob2::server::{Server, RecvType};
#[allow(unused_imports)]
use part2::prob2::client::Client;

// Use this file to write your own custom tests.
// Valid tests:
// - Write new valid tests below by naming your function valid_* and including
//   #[test] above each test.
//
// Invalid tests:
// - You can add new invalid tests by creating new test files in the same directory
//   and naming the files client_invalid_*.rs.
// - Each invalid test needs to include a main function with invalid uses of the TCP Client API.
//   Feel free to use the provided client_invalid_*.rs test files as templates (i.e. copy paste) for
//   the file structure and import statements.

// =========== TEST HELPER FUNCTIONS ===================
fn ids_equal(ids1: &Vec<u32>, ids2: &Vec<u32>) -> bool {
    if ids1.len() != ids2.len() {
        false
    } else {
        let mut ids1_c: Vec<u32> = ids1.clone();
        let mut ids2_c: Vec<u32> = ids2.clone();
        ids1_c.sort_by_key(|k| *k);
        ids2_c.sort_by_key(|k| *k);
        ids1_c.iter().eq(ids2_c.iter())
    }
}

fn extract_ids(pkts: &Vec<Pkt>) -> Vec<u32> {
    let mut ids: Vec<u32> = vec![];
    for pkt in pkts { ids.push((*pkt).id); }
    ids
}

// ============= TEST CASES BELOW ====================
// This is an example test (copied from the provided valid_01_send_syn_err test)
#[test]
fn valid_test_example() {
    // `server` fails to receive the first signal.
    let mut server: Server = Server::new(RecvType::Alter);
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => (),
        Ok (_syned) => assert!(false), // `send_syn` should fail.
    }
}

// DO NOT MODIFY. This test case ensures that all the invalid tests don't compile.
#[test]
fn invalid() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/prob2/custom/client_invalid_*.rs"); // compile should fail for these files.
}
extern crate part2;
#[allow(unused_imports)]
use part2::prob2::msg::Pkt;
#[allow(unused_imports)]
use part2::prob2::server::{Server, RecvType};
#[allow(unused_imports)]
use part2::prob3::sendall::send_all;

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

/**************
 * Test Cases *
 **************/
// TODO: write your own custom test cases here. You can use the provided tests as examples
// of how to write the tests.

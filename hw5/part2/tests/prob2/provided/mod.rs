extern crate part2;
#[allow(unused_imports)]
use part2::prob2::msg::Pkt;
#[allow(unused_imports)]
use part2::prob2::server::{Server, RecvType};
#[allow(unused_imports)]
use part2::prob2::client::Client;

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
#[test]
fn valid_01_send_syn_err() {
    // `server` fails to receive the first signal.
    let mut server: Server = Server::new(RecvType::Alter);
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => (),
        Ok (_syned) => assert!(false), // `send_syn` should fail.
    }
}

#[test]
fn valid_02_send_syn_ok() {
    // `server` receives all signals and packets.
    let mut server: Server = Server::new(RecvType::All);
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false), // `send_syn` should succeed.
        Ok (syned) => {
            // pkt-ids sent by client and pkt-ids recved by server should be `vec![]`.
            assert!(ids_equal(&vec![], &syned.ids_sent()));
            assert!(ids_equal(&vec![], &server.ids_recved()));
        }
    }
}

#[test]
fn valid_03_send_ack() {
    let mut server: Server = Server::new(RecvType::All);
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false),
        Ok (syned) => {
            let synacked = syned.send_ack(&mut server);
            // pkt-ids sent by client and pkt-ids recved by server should be `vec![]`.
            assert!(ids_equal(&vec![], &synacked.ids_sent()));
            assert!(ids_equal(&vec![], &server.ids_recved()));
        }
    }
}

#[test]
fn valid_04_send_pkts_once() {
    let mut server: Server = Server::new(RecvType::All);
    let pkts: Vec<Pkt> = vec![ Pkt{buf:'a', id:1}, Pkt{buf:'b', id:2} ];
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false),
        Ok (syned) => {
            let synacked = syned.send_ack(&mut server);
            let synacked = synacked.send_pkts(&mut server, &pkts);
            // pkt-ids sent by client and pkt-ids recved by server should be `pkts`.
            assert!(ids_equal(&extract_ids(&pkts), &synacked.ids_sent()));
            assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
        }
    }
}

#[test]
fn valid_05_send_pkts_twice() {
    let mut server: Server = Server::new(RecvType::All);
    let pkts: Vec<Pkt> = vec![ Pkt{buf:'a', id:1}, Pkt{buf:'b', id:2},
                               Pkt{buf:'c', id:4}, Pkt{buf:'d', id:3} ];
    let pkts1: Vec<Pkt> = pkts[0..2].to_vec();
    let pkts2: Vec<Pkt> = pkts[2..4].to_vec();
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false),
        Ok (syned) => {
            let synacked = syned.send_ack(&mut server);
            let synacked = synacked.send_pkts(&mut server, &pkts1);
            let synacked = synacked.send_pkts(&mut server, &pkts2);
            // pkt-ids sent by client and pkt-ids recved by server should be `pkts`.
            assert!(ids_equal(&extract_ids(&pkts), &synacked.ids_sent()));
            assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
        }
    }
}

#[test]
fn valid_06_send_close_ok() {
    let mut server: Server = Server::new(RecvType::All);
    let pkts: Vec<Pkt> = vec![ Pkt{buf:'a', id:1}, Pkt{buf:'b', id:2} ];
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false),
        Ok (syned) => {
            let synacked = syned.send_ack(&mut server);
            let synacked = synacked.send_pkts(&mut server, &pkts);
            match synacked.send_close(&mut server) {
                Err(_close_failed) => assert!(false), // `send_close` should succeed.
                Ok(closed) => {
                    // pkt-ids sent by client and pkt-ids recved by server should be `pkts`.
                    assert!(ids_equal(&extract_ids(&pkts), &closed.ids_sent()));
                    assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
                }
            }
        }
    }
}

#[test]
fn valid_07_send_ack() {
    let mut server: Server = Server::new(RecvType::All);
    let pkts: Vec<Pkt> = vec![ Pkt{buf:'a', id:1}, Pkt{buf:'b', id:2} ];
    let initial = Client::new();
    match initial.send_syn(&mut server) {
        Err(_syn_failed) => assert!(false),
        Ok (syned) => {
            let synacked = syned.send_ack(&mut server);
            let synacked = synacked.send_pkts(&mut server, &pkts);
            match synacked.send_close(&mut server) {
                Err(_close_failed) => assert!(false),
                Ok(closed) => {
                    let initial = closed.send_ack(&mut server);
                    // `ids_sent()` of a client should be set to empty,
                    // after the client returns back to the initial state.
                    assert!(ids_equal(&vec![], &initial.ids_sent()));
                    assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
                }
            }
        }
    }
}

#[test]
fn invalid() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/prob2/provided/client_invalid_*.rs"); // compile should fail for these files.
}

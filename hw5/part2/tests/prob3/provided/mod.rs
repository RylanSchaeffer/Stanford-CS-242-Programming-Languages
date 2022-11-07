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
#[test]
fn valid_01_all() {
    // `server` receives all signals and packets.
    let mut server: Server = Server::new(RecvType::All);
    let pkts: Vec<Pkt> = vec![
        Pkt { buf: 'a', id: 1 },
        Pkt { buf: 'b', id: 2 },
        Pkt { buf: 'c', id: 3 },
        Pkt { buf: 'd', id: 4 },
        Pkt { buf: 'e', id: 5 },
        Pkt { buf: 'f', id: 6 },
    ];

    send_all(&mut server, &pkts);

    // pkts recved by `server` should be `pkts`.
    assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
    // `server` should be disconnected from a client.
    assert!(!server.is_connected());
}

#[test]
fn valid_02_alter() {
    // `server` receives every other signal and packet.
    let mut server: Server = Server::new(RecvType::Alter);
    let pkts: Vec<Pkt> = vec![
        Pkt { buf: 'a', id: 1 },
        Pkt { buf: 'b', id: 2 },
        Pkt { buf: 'c', id: 3 },
        Pkt { buf: 'd', id: 4 },
        Pkt { buf: 'e', id: 5 },
        Pkt { buf: 'f', id: 6 },
    ];

    send_all(&mut server, &pkts);

    // pkts recved by `server` should be `pkts`.
    assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
    // `server` should be disconnected from a client.
    assert!(!server.is_connected());
}

#[test]
fn valid_03_rand() {
    // `server` receives signals and packets at random.
    let mut server: Server = Server::new(RecvType::Rand);
    let pkts: Vec<Pkt> = vec![
        Pkt { buf: 'a', id: 1 },
        Pkt { buf: 'b', id: 2 },
        Pkt { buf: 'c', id: 3 },
        Pkt { buf: 'd', id: 4 },
        Pkt { buf: 'e', id: 5 },
        Pkt { buf: 'f', id: 6 },
    ];

    send_all(&mut server, &pkts);

    // pkts recved by `server` should be `pkts`.
    assert!(ids_equal(&extract_ids(&pkts), &server.ids_recved()));
    // `server` should be disconnected from a client.
    assert!(!server.is_connected());
}

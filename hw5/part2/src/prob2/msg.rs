/* DO NOT EDIT THIS FILE. */

/***************
 * NOTE:
 *   To implement `client.rs`, you only need to understand
 *   the definition of `Sig` and `Pkt`.
 *   You do not need to understand other parts.
 ***************/

use std::fmt;

/**************************
 * Defn of Signal, Packet *
 **************************/
pub enum Sig {
    Syn, SynAck, Ack, Close, CloseAck,
}

#[derive(Clone, PartialEq, Copy)]
pub struct Pkt {
    pub buf: char,
    pub id : u32,
}

/*************************
 * Ops on Signal, Packet *
 *************************/
impl fmt::Debug for Pkt {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "(buf: '{}', id: {})", self.buf, self.id)
    }
}

impl fmt::Debug for Sig {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let text: &str =
            match self {
                Sig::Syn      => "Sig::Syn",
                Sig::SynAck   => "Sig::SynAck",
                Sig::Ack      => "Sig::Ack",
                Sig::Close    => "Sig::Close",
                Sig::CloseAck => "Sig::CloseAck",
            };
        write!(f, "{}", text)
    }
}
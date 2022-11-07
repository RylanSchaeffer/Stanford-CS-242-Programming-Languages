/***************
 * NOTE:
 *   You can call `internal_login` simply by `internal_login(id, pw)`.
 ***************/

#[allow(unused_imports)]
use crate::prob1::server::internal_login;

// TODO: Implement the following typestate structs. You are free to add any fields to the struct
// definitions.
// Below shows the signature of the methods to be implemented across the cart state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn login(_: String, _: String) -> Result<T,()>
//   pub fn add_item(self, _: u32) -> T
//   pub fn clear_items(self) -> T
//   pub fn checkout(self) -> T
//   pub fn cancel(self) -> T
//   pub fn order(self) -> T
//   pub fn acct_num(&self) -> u32
//   pub fn tot_cost(&self) -> u32
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Cart {}
pub struct Empty {}
pub struct NonEmpty {}
pub struct Checkout {}

//===== END_CODE =====//

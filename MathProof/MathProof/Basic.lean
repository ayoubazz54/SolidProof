import Mathlib

example (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b

use pyo3::prelude::*;
use tools_2048::Game2048;

#[pyfunction]
fn new_game() -> ([[u32; 4]; 4], Vec<usize>) {
    // (board, moves)
    let game = Game2048::new();
    (game.board, game.moves)
}

#[pyfunction]
fn make_move(board: [[u32; 4]; 4], move_type: usize) -> ([[u32; 4]; 4], Vec<usize>, usize) {
    // (board, moves, move_result)
    let mut game = Game2048::from_existing(board);
    let move_result = game.make_move(move_type);
    (game.board, game.moves, move_result)
}

#[pyfunction]
fn make_best_move(board: [[u32; 4]; 4], depth: usize) -> ([[u32; 4]; 4], Vec<usize>, usize) {
    // (board, moves, move_result)
    let mut game = Game2048::from_existing(board);
    let move_result = game.make_move(game.find_best_move(depth));
    (game.board, game.moves, move_result)
}

#[pymodule]
fn rust_2048(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(new_game, m)?)?;
    m.add_function(wrap_pyfunction!(make_move, m)?)?;
    m.add_function(wrap_pyfunction!(make_best_move, m)?)?;
    Ok(())
}

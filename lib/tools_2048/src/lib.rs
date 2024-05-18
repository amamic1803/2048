use pyo3::exceptions::PyException;
use pyo3::prelude::*;
use tools_2048_cratesio::{Error, Game, GameMove, GameResult, GameState};

// error wrapper
struct ErrorWrapper(Error);
impl From<Error> for ErrorWrapper {
    fn from(error: Error) -> Self {
        Self(error)
    }
}
impl From<ErrorWrapper> for PyErr {
    fn from(error: ErrorWrapper) -> Self {
        PyException::new_err(error.0.to_string())
    }
}

/// A class that represents the 2048 game.
#[pyclass]
struct Game2048(Game<4>);

#[pymethods]
impl Game2048 {
    /// Creates a new game of 2048.
    #[new]
    fn new() -> Self {
        Self(Game::<4>::new().unwrap())
    }

    /// Creates a game of 2048 from an existing board.
    /// # Arguments
    /// * ```board```: The board to use.
    /// * ```score```: The score of the game.
    /// # Exceptions
    /// * ```Exception```: If the size of the board is invalid. Must be at least 4.
    /// * ```Exception```: If the board is invalid. Must be quadratic.
    /// * ```Exception```: If the board contains invalid values. Must be 0 or powers of 2 (except 1).
    #[staticmethod]
    fn from_existing(board: [[u64; 4]; 4], score: u64) -> Result<Self, ErrorWrapper> {
        Ok(Self(Game::from_existing(&board, score)?))
    }

    /// Returns the board of the game.
    fn board(&self) -> [[u64; 4]; 4] {
        *self.0.board()
    }

    /// Returns the result of the game.
    /// # Returns
    /// * ```1```: The game is won, 2048 was reached.
    /// * ```0```: The game is in progress, 2048 is not reached yet.
    /// * ```-1```: The game is over, 2048 was not reached.
    fn result(&self) -> i8 {
        match self.0.result() {
            GameResult::Victory => 1,
            GameResult::Pending => 0,
            GameResult::Loss => -1,
        }
    }

    /// Returns the score of the game.
    fn score(&self) -> u64 {
        self.0.score()
    }

    /// Returns the size of the board.
    fn size(&self) -> usize {
        4
    }

    /// Returns the state of the game.
    /// # Returns
    /// * ```0```: The game is in progress.
    /// * ```1```: The game is over.
    fn state(&self) -> i8 {
        match self.0.state() {
            GameState::InProgress => 0,
            GameState::GameOver => 1,
        }
    }

    /// Make a move in the game.
    /// # Arguments
    /// * ```direction```: The direction to move in. 0 = left, 1 = right, 2 = up, 3 = down.
    /// # Returns
    /// * ```true``` - The move was successful.
    /// * ```false``` - The move was invalid/impossible.
    fn make_move(&mut self, direction: u8) -> bool {
        self.0.make_move(match direction {
            0 => GameMove::Left,
            1 => GameMove::Right,
            2 => GameMove::Up,
            3 => GameMove::Down,
            _ => return false,
        })
    }

    /// Find the best move to make based on the current board state.
    /// Based on Monte Carlo algorithm (randomized guessing).
    /// Uses multiple threads to speed up the process.
    /// # Arguments
    /// * ```depth``` - The number of simulated games to play to determine the best move. Recommended value is 1000.
    /// # Returns
    /// * ```n``` - The best move to make. 0 = left, 1 = right, 2 = up, 3 = down.
    /// # Exceptions
    /// * ```Exception``` - If there are no valid moves left.
    fn find_best_move(&self, depth: usize) -> Result<u8, ErrorWrapper> {
        Ok(match self.0.find_best_move(depth)? {
            GameMove::Left => 0,
            GameMove::Right => 1,
            GameMove::Up => 2,
            GameMove::Down => 3,
        })
    }
}

#[pymodule]
fn tools_2048(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Game2048>()?;
    Ok(())
}

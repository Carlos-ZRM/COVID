// https://gist.github.com/lizzybrooks/54045563e4e8321718cc40297db999f9

//inputs
let rows_i, cols_i, dist_i, rule_i, memory_i;

//buttons
let autmatic_btn, manual_btn, begin_btn, file_btn, graph_btn, atractor_btn;
let pattern_1_btn, patternt_2_btn, pattern_3_btn, pattern_4_btn, pattern_5_btn;

//configurationf of the grid
let resolution = 5;
let started = false;
let manual = false;
let automatic = false;
let color_background = [0, 0, 0];
let color_cell = [255, 255, 255];

//gol global variables
let grid, rows, cols, manual_rows, manual_cols, global_prob;
let generation = 0;
let rule = 0;
let is_draw = false;
let r1, r2, r3, r4;

//Attractors
var lookup_nodes = new Map();
let prev_attractor = -1;
let number_of_configurations = 0;
let current_configuration = 0;
let is_atractor_mode = false;

//Count patterns
let global_patterns;
let counter_of_patterns = [0, 0, 0];

//Draw patterns
let current_pattern = 0;
let is_pattern = false;
let grid_pattern = [];

//Memory rule
let memory_grid;
let memory_limit = 0;
let memory_counter = 0;

function setup() {
  createCanvas(500, 500);

  rows_txt = createP("Número de Filas:");
  rows_txt.position(20, 10);

  rows_i = createInput("300");
  rows_i.position(200, 20);
  rows_i.size(90, 20);

  cols_txt = createP("Número de Columnas:");
  cols_txt.position(20, 50);

  cols_i = createInput("300");
  cols_i.position(200, 60);
  cols_i.size(90, 20);

  dist_txt = createP("Prob. de 0:");
  dist_txt.position(400, 50);

  dist_i = createInput("50");
  dist_i.position(490, 60);
  dist_i.size(90, 20);

  rule_txt = createP("Regla:");
  rule_txt.position(430, 10);

  rule_i = createInput("2333");
  rule_i.position(490, 20);
  rule_i.size(90, 20);

  memory_txt = createP("Número de memoria:");
  memory_txt.position(760, 0);

  memory_i = createInput("4");
  memory_i.position(920, 10);
  memory_i.size(50, 20);

  autmatic_btn = createButton("Generación Automática");
  autmatic_btn.position(20, 110);
  autmatic_btn.mousePressed(randomGeneration);

  manual_btn = createButton("Generación Manual");
  manual_btn.position(205, 110);
  manual_btn.mousePressed(manualGeneration);

  file_btn = createButton("Leer De Archivo");
  file_btn.position(368, 110);
  file_btn.mousePressed(readFromFile);

  graph_btn = createButton("Graficar");
  graph_btn.position(515, 110);
  graph_btn.mousePressed(graphInitialConfiguration);

  begin_btn = createButton("Comenzar");
  begin_btn.position(625, 110);
  begin_btn.mousePressed(beginGame);

  atractor_btn = createButton("Atractor");
  atractor_btn.position(750, 110);
  atractor_btn.mousePressed(beginAttractor);

  pattern_1_btn = createButton("P1");
  pattern_1_btn.position(20, 160);
  pattern_1_btn.mousePressed(function() {
    setPatternConfiguration(1);
  });

  pattern_2_btn = createButton("P2");
  pattern_2_btn.position(80, 160);
  pattern_2_btn.mousePressed(function() {
    setPatternConfiguration(2);
  });

  pattern_3_btn = createButton("P3");
  pattern_3_btn.position(140, 160);
  pattern_3_btn.mousePressed(function() {
    setPatternConfiguration(3);
  });

  pattern_4_btn = createButton("P4");
  pattern_4_btn.position(200, 160);
  pattern_4_btn.mousePressed(function() {
    setPatternConfiguration(4);
  });

  pattern_5_btn = createButton("P5");
  pattern_5_btn.position(260, 160);
  pattern_5_btn.mousePressed(function() {
    setPatternConfiguration(5);
  });

  createDiv("").id("content");
  rows_txt.parent("content");
  rows_i.parent("content");
  cols_txt.parent("content");
  cols_i.parent("content");
  rule_i.parent("content");
  autmatic_btn.parent("content");
  manual_btn.parent("content");
  memory_txt.parent("content");
  memory_i.parent("content");
  begin_btn.parent("content");
  rule_txt.parent("content");
  file_btn.parent("content");
  graph_btn.parent("content");
  atractor_btn.parent("content");
  pattern_1_btn.parent("content");
  pattern_2_btn.parent("content");
  pattern_3_btn.parent("content");
  pattern_4_btn.parent("content");
  pattern_5_btn.parent("content");

  dist_i.parent("content");
  dist_txt.parent("content");

  textAlign(CENTER);
  textSize(20);

  localStorage.setItem("started", 0);
  global_patterns = createHashOfPatterns();

  noLoop();
}

function beginAttractor() {
  num_of_rows = parseInt(rows_i.value());

  setGlobalRowsCols(num_of_rows, num_of_rows);
  resolutions = getNewResolution(num_of_rows, num_of_rows, resolution);
  resizeCanvas(resolutions[0], resolutions[1]);

  number_of_configurations = Math.pow(2, num_of_rows * num_of_rows);
  lookup_nodes = createHashmap(number_of_configurations);
  grid = getGridConfiguration(
    current_configuration,
    num_of_rows * num_of_rows,
    num_of_rows
  );

  is_atractor_mode = true;
}

function randomGeneration() {
  num_of_rows = parseInt(rows_i.value());
  num_of_cols = parseInt(cols_i.value());
  global_prob = parseInt(dist_i.value());

  resolutions = getNewResolution(num_of_rows, num_of_cols, resolution);
  setGlobalRowsCols(num_of_rows, num_of_cols);
  resizeCanvas(resolutions[0], resolutions[1]);

  grid = make2DArray(rows, cols);
  grid = changeProb(global_prob);
}

function manualGeneration() {
  n_rows = parseInt(rows_i.value());
  n_cols = parseInt(cols_i.value());
  manual = true;

  setGlobalRowsCols(n_rows, n_cols);
  resizeCanvas(windowWidth, 150);

  grid = make2DArray(n_rows, n_cols);
  createManualGrid(n_rows, n_cols, grid);
}

function graphInitialConfiguration() {
  let ones_fg = countOnesFirstGeneration(grid);
  localStorage.setItem("number", ones_fg);
  localStorage.setItem("generation", generation);
  localStorage.setItem("patterns", counter_of_patterns);
  localStorage.setItem("started", true);
}

function beginGame() {
  //memory
  /*
  memory_grid = grid.map(function (arr) {
    return arr.slice();
  });*/
  memory_grid = make2DArrayZeros(rows, cols);
  memory_limit = parseInt(memory_i.value());

  localStorage.setItem("number", 0);
  localStorage.setItem("generation", 0);

  if (document.getElementById("automatic").checked) {
    automatic = true;
  }

  color_background = hexToRgb(
    document.getElementById("background-color").value
  );
  color_cell = hexToRgb(document.getElementById("cell-color").value);

  document.getElementById("content").style.display = "none";
  document.getElementById("content").style.visibility = "hidden";
  document.getElementById("myForm").style.display = "none";
  document.getElementById("automatic").style.display = "none";
  document.getElementById("background-color").style.display = "none";
  document.getElementById("cell-color").style.display = "none";

  //r1,r2,r3,r4
  generalRule = rule_i.value();
  r4 = generalRule % 10;
  generalRule = Math.floor(generalRule / 10);
  r3 = generalRule % 10;
  generalRule = Math.floor(generalRule / 10);
  r2 = generalRule % 10;
  generalRule = Math.floor(generalRule / 10);
  r1 = generalRule;

  if (manual == true) {
    resolutions = getNewResolution(rows, cols, resolution);
    resizeCanvas(resolutions[0], resolutions[1]);
    document.getElementById("manual_grid").style.display = "none";
  }

  //Delay the appereance of the grid
  setTimeout(loop, 1);
  started = true;
  is_draw = true;

  localStorage.setItem("started", true);
}

function draw() {
  if (started) {
    background(color_background[0], color_background[1], color_background[2]);

    let next = make2DArray(rows, cols);
    let number_of_ones = 0;

    //Attractors
    let current_node = [];
    if (is_atractor_mode == true) {
      current_node = flatarray(grid);
    }

    //Memory
    if (memory_limit != 0) {
      memory_counter += 1;
    }

    for (let i = 0; i < grid.length; i++) {
      for (let j = 0; j < grid[0].length; j++) {
        let x = i * resolution;
        let y = j * resolution;

        if (grid[i][j] == 1) {
          fill(color_cell[0], color_cell[1], color_cell[2]);
          stroke(0);
          rect(y, x, resolution - 1, resolution - 1);
          number_of_ones += 1;
        }

        let state = grid[i][j];
        let neighbors_information = countNeighbors(grid, i, j);
        let neighbors = neighbors_information[0];
        let pattern = neighbors_information[1];

        incrementConfiguration(pattern);

        if (state == 0 && (neighbors >= r3 && neighbors <= r4)) {
          next[i][j] = 1;
        } else if (state == 1 && (neighbors < r1 || neighbors > r2)) {
          next[i][j] = 0;
        } else {
          next[i][j] = state;
        }

        //memory
        if (memory_limit != 0) {
          if (state == 1) {
            memory_grid[i][j] += 1;
          }
        }
      }
    }

    localStorage.setItem("number", number_of_ones);
    localStorage.setItem("generation", generation);
    localStorage.setItem("patterns", counter_of_patterns);

    grid = next;

    if (memory_limit != 0) {
      if (memory_limit == memory_counter) {
        let number_of_ones_mem = 0;
        let temporal_memories = make2DArray(rows, cols);
        let median_elements = Math.floor(memory_limit / 2);

        for (let m_row = 0; m_row < memory_grid.length; m_row++) {
          for (let m_col = 0; m_col < memory_grid[0].length; m_col++) {
            if (memory_grid[m_row][m_col] >= median_elements) {
              temporal_memories[m_row][m_col] = 1;
              number_of_ones_mem += 1;
            } else {
              temporal_memories[m_row][m_col] = 0;
            }
            memory_grid[m_row][m_col] = 0;
          }
        }

        localStorage.setItem("number_mem", number_of_ones_mem);

        let next_memory = make2DArray(rows, cols);
        for (let m_row = 0; m_row < temporal_memories.length; m_row++) {
          for (let m_col = 0; m_col < temporal_memories[0].length; m_col++) {
            let mem_state = temporal_memories[m_row][m_col];
            let mem_neighbors_information = countNeighbors(
              temporal_memories,
              m_row,
              m_col
            );
            let mem_neighbors = mem_neighbors_information[0];
            let mem_pattern = mem_neighbors_information[1];

            incrementConfiguration(mem_pattern);

            if (
              mem_state == 0 &&
              (mem_neighbors >= r3 && mem_neighbors <= r4)
            ) {
              next_memory[m_row][m_col] = 1;
            } else if (
              mem_state == 1 &&
              (mem_neighbors < r1 || mem_neighbors > r2)
            ) {
              next_memory[m_row][m_col] = 0;
            } else {
              next_memory[m_row][m_col] = mem_state;
            }
          }
        }

        grid = next_memory;
        memory_counter = 0;
      } else {
        localStorage.setItem("number_mem", 0);
      }
    }

    //Attractor
    if (is_atractor_mode == true) {
      let next_node = flatarray(grid);
      nodes = lookup_nodes.get(current_node);
      if (!nodes.has(next_node)) {
        nodes.add(next_node);
        lookup_nodes.set(current_node, nodes);
      } else if (current_node == next_node) {
        if (current_configuration < number_of_configurations - 1) {
          current_configuration += 1;
          grid = getGridConfiguration(
            current_configuration,
            num_of_rows * num_of_rows,
            num_of_rows
          );
        } else {
          started = false;
          createJSONFromMap(lookup_nodes);
        }
      } else {
        if (current_configuration < number_of_configurations - 1) {
          current_configuration += 1;
          grid = getGridConfiguration(
            current_configuration,
            num_of_rows * num_of_rows,
            num_of_rows
          );
        } else {
          started = false;
          createJSONFromMap(lookup_nodes);
        }
      }
    }

    generation += 1;
    counter_of_patterns = [0, 0, 0];
    if (automatic == false) {
      started = false;
    }
  }
}

function mouseClicked() {
  if (is_draw == true) {
    started = !started;
    localStorage.setItem("started", started);
  }
}

function readFromFile() {
  loadStrings("input.txt", fileLoaded);
}

function fileLoaded(data) {
  let arr = new Array(data.length);
  let cols = Array.from(data);

  for (let i = 0; i < cols.length; i++) {
    let tmp = Array.from(cols[i]);
    let result = tmp.map(Number);
    arr[i] = Array.from(result);
  }

  grid = arr;
  resolutions = getNewResolution(grid.length, grid[0].length, resolution);
  setGlobalRowsCols(grid.length, grid[0].length);
  resizeCanvas(resolutions[0], resolutions[1]);
}

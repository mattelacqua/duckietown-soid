import './Header.css'

import React from "react";

const Header = () => {
  return (
    <div className="head">
      <div className="headText">
        <h1> soid: SMT-based Oracles for Investigating Decisions </h1>
        <h2> A Car Crash Investigation: Demonstration & GUI </h2>
        <p> This is a demonstration of <b>soid</b>, a tool for applying automated reasoning to principled accountability for algorithmic decision making. It is produced by the <a href='https://rose.yale.edu/'>Rigorous Software Engineering (ROSE)</a> group from Department of Computer Science at Yale, in collaboration with researchers from <a href="https://law.yale.edu/">Yale Law School</a> and the <a href="https://www.iaik.tugraz.at/">Institute of Applied Information Processing and Communications</a> at TU-Graz.</p>

        <p>This GUI, built on top of the <a href="https://github.com/duckietown/gym-duckietown">Gym-Duckietown</a> project, is designed for interactive investigations of car crashes. The goal of <b>soid</b> is to enable iterative, human expert-directed analysis of the <i>purpose</i> of an agent's decisions at critical moments in the run up to a crash. These <i>present-directed intentions</i> are critical to understanding an agent's responsibility for the crash, and assessing them is often required by accountability processes such as legal proceedings.</p>

        <p>At left is the state of the world. It is the blue car (or agent0) that is 'under investigation'. At right is a drag-and-drop interface for manipulating the location of cars. Below, additional cars can be added and the orientation, direction of travel, and order of intersection arrival (for calculating right-of-way) of all cars can be manipulated. In addition, the machine learned (via reinforcement learning) decision logic to be used by the blue car can be selected.</p>

        <p>After an execution is paused, the Log Step slider can be used to select a critical moment of the blue car's decision making. The counterfactual menus under each agent can be used to specify (families of) hypothetical, alternative scenario(s), and then <b>soid</b> can be queried to determine whether the blue car might or would have moved under (any of) the scenario(s). Behind the scenes, <b>soid</b> uses the <a href="https://www.microsoft.com/en-us/research/project/z3-3/">Z3</a> SMT solver to resolve all queries.</p>

        <p><a href="https://arxiv.org/abs/2305.05731">arXiv</a><br />
        <a href="https://github.com/sjudson/soid">Github (soid)</a><br />
        <a href="https://github.com/mattelacqua/duckietown-soid">Github (soid-gui)</a></p>
      </div>
    </div>
  );
};

export default Header;

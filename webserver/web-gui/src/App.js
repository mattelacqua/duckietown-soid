// Import styplesheet for App
import './App.css';

// Import React for components
import React from 'react'

// Import Agents since it will be rendered in appb
import Agents from './Agents.js'

// Import Environment since it will be rendered in app
import Environment from './Environment.js'

// Import Agentmpa
import AgentMap from './AgentMap.js'

// Import RenderedScene
import RenderedScene from './RenderedScene.js'

// Import RenderedScene
import Buttons from './Buttons.js'

// Import LODASH
import _ from 'lodash';

// Import Socket IO
import io from 'socket.io-client';

// Create the socket
const socket = io();

// Our top level class (gets rendered in index.html)
class App extends React.Component{

    // Constructor for component (set up what our App's state is)
    constructor(props) {
        super(props);
   
        // State contains a list of agents (json format), and a bool for if the data loaded
        this.state = {
            agents: [],
            env_info: [],
            AgentsLoaded: false,
            EnvLoaded: false,
            rendred_imgLoaded: false,
            rendered_img: new Image(),
            sim_state: '',
            socket: socket,
        };
        this.update_from_sim = this.update_from_sim.bind(this); // Bind this to update_from sim 
    }

    // Update from the simulator
    update_from_sim() {
      socket.emit("update_sim_info");
      // Fetch for env info
      fetch("/envInfo") // Shorthand for http://localhost:5000/agetns
          .then((res) => res.json()) // Result becomes a json
          .then((json) => { // take the json and set the state vars with it
              let new_ref = json;
              if (!_.isEqual(new_ref, this.state.env_info)) {
                console.log("Old State: ", this.state.env_info.state);
                console.log("New State: ", new_ref.state);
                this.setState({
                    env_info: new_ref,
                    agents: new_ref.agents,
                    EnvLoaded: true,
                    sim_state: new_ref.state
                });
              } // Endif
          });

      // Get the rendered image
      const image = new Image();
      image.src = 'http://localhost:5001/renderedScene';

      this.setState({
        rendered_img: image,
        rendered_imgLoaded: true
      });

      this.forceUpdate();

    }
  
    // When we renderour App, fetch the agent information
    componentDidMount() {
      this.update_from_sim();
      console.log("updating from sim");
      this.interval = setInterval(() => this.update_from_sim(), 2000);
    }
   
    // Render Our App Component ( calls to Agent subchildren)
    render() {
        
      //console.log("Rerender From Top. Current State:", this.state.sim_state);
        // If our data didn't load, lets write HTML that we are waiting 
        if ((!this.state.EnvLoaded) ||
           (!this.state.rendered_imgLoaded))
           return <div> 
            <h1> Loading Simpulation information ... </h1> 
            <h1> Please ensure that the simulator and webserver are running ... </h1> 
        </div> ;

        // When our data is loaded, we want to return the HTML/REACT Calls for the APP
        return (

        // Div to clump app up into one component to render
        <div className = "App"> {/* Using app.css stylesheet */}
            {/* Header text */}
            <div className="Modify-wrap">
              <RenderedScene />
              <Environment  max_NS={this.state.env_info.grid_h * this.state.env_info.road_tile_size} 
                            max_EW={this.state.env_info.grid_w * this.state.env_info.road_tile_size}
                            tile_size={this.state.env_info.road_tile_size}
                            sim_state={this.state.sim_state}
                            socket={this.state.socket}
                            sim_step={this.state.env_info.sim_step}/>

              <Buttons sim_state={this.state.sim_state} 
                       update_from_sim={this.update_from_sim}
                       socket={this.state.socket}/>

              {this.state.sim_state === 'pause' && 
                  <AgentMap agents={this.state.agents} 
                          max_NS={this.state.env_info.grid_h * this.state.env_info.road_tile_size} 
                          max_EW={this.state.env_info.grid_w * this.state.env_info.road_tile_size} 
                          tile_size={this.state.env_info.road_tile_size}
                          socket={this.state.socket}/> 

              }
            </div>

            <div className="Agents-wrap">
              {this.state.sim_state === 'pause' && 
                  <Agents agents={this.state.agents}
                          socket={this.state.socket}/>
              }
            </div>
        </div>
    ); // End of return
}
}


// Allow it to be called in other functions
export default App;

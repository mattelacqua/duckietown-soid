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

const headers = new Headers();
headers.set('Accept', '*');
headers.set('Access-Control-Allow-Credentials', 'true');
headers.set('Access-Control-Allow-Origin', 'true');
headers.set('Content-Type', 'application/json');

// Our top level class (gets rendered in index.html)
class App extends React.Component{

    // Constructor for component (set up what our App's state is)
    constructor(props) {
        super(props);
   
        // State contains a list of agents (json format), and a bool for if the data loaded
        this.state = {
            env_info: [],
            EnvLoaded: false,
            rendred_imgLoaded: false,
            rendered_img: new Image(),
            sim_state: '',
            socket: socket,
        };
        this.update_from_sim = this.update_from_sim.bind(this); // Bind this to update_from sim 
    }

    // Update from the simulator
    async update_from_sim() {
      socket.emit("update_sim_info");
      console.log("UPDATING FROM SIM");
      console.log("headers:", headers)
      // Fetch for env info
      const response = await fetch("/envInfo.json",{ headers : headers} 
       ) // Shorthand for http://localhost:5000/agetns
          .then(res => res.json()) // Result becomes a json
          .then(result => 
          {console.log(result)
          
              let new_ref = result;
              if (!_.isEqual(new_ref, this.state.env_info)) {
                this.setState({
                    env_info: new_ref,
                    EnvLoaded: true,
                    sim_state: new_ref.state
                });
                console.log("Got new info", new_ref);
              } // Endif
          }) 
          .catch(error => console.log('error', error));  // take the json and set the state vars with it


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
            <h1> Loading Simulation information ... </h1> 
            <h1> Please ensure that the simulator and webserver are running ... </h1> 
        </div> ;
        else {
          //console.log("LOADED BUT RENDER ISSUES?")

        }

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
                       env_info={this.state.env_info}
                       socket={this.state.socket}/>

              {this.state.sim_state === 'pause' && 
                  <AgentMap agents={this.state.env_info.agents} 
                          max_NS={this.state.env_info.grid_h * this.state.env_info.road_tile_size} 
                          max_EW={this.state.env_info.grid_w * this.state.env_info.road_tile_size} 
                          tile_size={this.state.env_info.road_tile_size}
                          socket={this.state.socket}/> 

              }
            </div>

            <div className="Agents-wrap">
              {this.state.sim_state === 'pause' && 
                  <Agents agents={this.state.env_info.agents}
                          socket={this.state.socket}
                          update_from_sim={this.update_from_sim}/>
              }
            </div>
        </div>
    ); // End of return
}
}


// Allow it to be called in other functions
export default App;

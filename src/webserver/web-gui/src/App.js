// Import styplesheet for App
import './App.css';

// Import React for components
import React from 'react'
import ReactModal from 'react-modal'

import Header from './Header.js'
import Footer from './Footer.js'

// Import Agents since it will be rendered in appb
import Agents from './agents/Agents.js'
import AgentMap from './agents/AgentMap.js'

// Import RenderedScene
import RenderedScene from './environment/RenderedScene.js'

// Import CounterfactualModal
import CounterfactualModal from './agents/counterfactual/CounterfactualModal.js'

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
        rendered_imgLoaded: false,
        rendered_img: new Image(),
        sim_state: '',
        socket: socket,
        started: false,
      };
      this.update_from_sim = this.update_from_sim.bind(this); // Bind this to update_from sim
  }

  // Update from the simulator
  async update_from_sim() {
    socket.emit("update_sim_info");

    let ref;

    // Fetch for env info
    await fetch("/envInfo.json", {headers: headers}) // Shorthand for http://127.0.0.1:5001/envInfo.json
      .then(res => res.json()) // Result becomes a json
      .then(result =>
        { ref = result;
          if (!_.isEqual(ref, this.state.env_info)) {
            this.setState({
              env_info: ref,
              EnvLoaded: true,
              sim_state: ref.state,
              started: ref.started
            });
          } // Endif
      })
      .catch(error => console.log('error catching env_info', error));  // take the json and set the state vars with it

    // Get the rendered image
    const image = new Image();
    image.src = 'http://127.0.0.1:5001/renderedScene';

    this.setState({
      rendered_img: image,
      rendered_imgLoaded: true
    });

    this.forceUpdate();

    return ref;
  }

  // When we renderour App, fetch the agent information
  componentDidMount() {
    this.update_from_sim();
    this.interval = setInterval(() => this.update_from_sim(), 2000);
  }

  // Render Our App Component ( calls to Agent subchildren)
  render() {
    // If our data didn't load, lets write HTML that we are waiting
    if ((!this.state.EnvLoaded) ||
        (!this.state.rendered_imgLoaded))
        return <div>
                <h1> Loading Simulation Information ... </h1>
                <h1> Please ensure that the simulator and webserver are running ... </h1>
               </div> ;

    // When our data is loaded
    return (
      // Div to clump app up into one component to render
      <>
        <Header />
        <CounterfactualModal
          query_info={this.state.env_info.query_info}
          agents={this.state.env_info.agents}
          socket={this.state.socket} />
        <div className="App">
          <div className="Modify-wrap">
            <RenderedScene sim_state={this.state.sim_state}
                           sim_step={this.state.env_info.sim_step}
                           socket={this.state.socket}
                           max_NS={this.state.env_info.grid_h * this.state.env_info.road_tile_size}
                           max_EW={this.state.env_info.grid_w * this.state.env_info.road_tile_size}
                           tile_size={this.state.env_info.road_tile_size}
                           update_from_sim={this.update_from_sim}
                           started={this.state.started} />
            <AgentMap agents={this.state.env_info.agents}
                      max_NS={this.state.env_info.grid_h * this.state.env_info.road_tile_size}
                      max_EW={this.state.env_info.grid_w * this.state.env_info.road_tile_size}
                      tile_size={this.state.env_info.road_tile_size}
                      socket={this.state.socket} />
          </div>
          <Agents agents={this.state.env_info.agents}
                  socket={this.state.socket}
                  sim_state={this.state.sim_state}
                  sim_step={this.state.env_info.sim_step}
                  env_info={this.state.env_info}
                  update_from_sim={this.update_from_sim}
                  started={this.state.started} />
          {/*End of running */}
        </div>
        <Footer />
      </>
    ); // End of return
  }
}

// Allow it to be called in other functions
export default App;

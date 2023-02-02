import React from "react";
import './Buttons.css';


// Component to spit out agent information
class Buttons extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
        sim_state: this.props.sim_state,
        socket: this.props.socket
    };
    this.handleClick = this.handleClick.bind(this);
  }
  
  // Handle the click
  async handleClick(state) {
    if (state !== "add_agent" && state !=="query") {

      this.setState({
        sim_state: state,
      });

      if (state === 'pause') {
          console.log("Emitting update_sim_info");
          this.state.socket.emit('update_sim_info');
          setTimeout(this.props.update_from_sim(), 1000);
      }

      console.log("Emitting sim_state", state);
      this.state.socket.emit('sim_state', {'state':state});
    } else {
        if (state === "add_agent"){
          this.state.socket.emit('add_agent');
        }
        if (state === "query"){
          const delay = ms => new Promise(res => setTimeout(res, ms));
          this.props.update_from_sim();
          await delay(2000)
          this.props.update_from_sim();
          
          // Add the counterfactuals to the queryy
          console.log('ENV INFO FOR QUERY:', this.props.env_info);
          this.state.socket.emit('query', 
            {
              'query': {
                'is_factual': false ,
                'is_existential': false ,
                'behavior': 'CHANGE ME TO QUERY BEHAVIOR' ,
              },
              'env_info': this.props.env_info
            }
            );
          console.log("Sending this as a query", this.props.env_info);
        }
  }
}
  
  // Render the information to screen
  render() {
    return (
      <div class='Buttons'>

          {this.props.sim_state === 'run' &&
            <button className='pause' onClick={()=>this.handleClick("pause")}>Pause</button>
          }
          {this.props.sim_state === 'run' &&
            <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>
          }
         {this.props.sim_state === 'pause' &&
            <button className='add_agent' onClick={()=>this.handleClick("add_agent")}>Add New Agent</button>
         }
         {this.props.sim_state === 'pause' &&
            <button className = "resume" onClick={()=>this.handleClick("run")}>Resume</button>
         }
         {this.props.sim_state === 'pause' &&
            <button className='quit' onClick={()=>this.handleClick("quit")}>Quit</button>
         }
          {this.props.sim_state === 'pause' &&
            <button className='query' onClick={()=>this.handleClick("query")}>Send Query</button>
         }
      </div>
      );
    }
}

export default Buttons;
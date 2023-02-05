import React from "react";
import './Queries.css';


// Component to spit out agent information
class Queries extends React.Component {

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
    if (state !== "add_agent" && state !== "move_factual" && state !== 'move_existential' && state !== "stop_factual" && state !== 'stop_existential') {

      this.setState({
        sim_state: state,
      });

      const delay = ms => new Promise(res => setTimeout(res, ms));
      this.props.update_from_sim();
      await delay(2000)
      this.props.update_from_sim();
      
      // Add the counterfactuals to the queryy
      console.log('ENV INFO FOR QUERY:', this.props.env_info);
      if (state === "move_factual"){

        this.state.socket.emit('query', 
          {
            'query': {
              'is_factual': true ,
              'is_existential': false ,
              'behavior': 'move' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      else if (state === "move_existential"){

        this.state.socket.emit('query', 
          {
            'query': {
              'is_factual': false ,
              'is_existential': true ,
              'behavior': 'move' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      else if (state === "stop_factual"){

        this.state.socket.emit('query', 
          {
            'query': {
              'is_factual': true ,
              'is_existential': false ,
              'behavior': 'stop' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
      if (state === "stop_existential"){

        this.state.socket.emit('query', 
          {
            'query': {
              'is_factual': false ,
              'is_existential': true ,
              'behavior': 'stop' ,
            },
            'env_info': this.props.env_info
          }
          );
      }
    }
  }
  
  // Render the information to screen
  render() {
    return (
      <div> 
        <p style={{
        display: 'flex',
        paddingTop: '2em',
      }}> Ask a Question based on given Counterfactuals:</p>
        <div class='Queries'>
            {this.props.sim_state === 'pause' &&
              <button className='move_factual' onClick={()=>this.handleClick("move_factual")}>Agent Always Moves?</button>
          }
            {this.props.sim_state === 'pause' &&
              <button className='move_existential' onClick={()=>this.handleClick("move_existential")}>Agent Could Move?</button>
          }
        </div>
        <div class='Queries'>
            {this.props.sim_state === 'pause' &&
              <button className='stop_factual' onClick={()=>this.handleClick("stop_factual")}>Agent Always Stops?</button>
          }
            {this.props.sim_state === 'pause' &&
              <button className='stop_existential' onClick={()=>this.handleClick("stop_existential")}>Agent Could Stop?</button>
          }
        </div>
      </div>
      );
    }
}

export default Queries;
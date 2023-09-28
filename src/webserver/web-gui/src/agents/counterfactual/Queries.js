import React from "react";
import './Queries.css';


// Component to spit out agent information
class Queries extends React.Component {

  // Construct so it takes properties and they are information
  constructor(props) {
    super(props);
    this.state = {
    };
    this.handleClick = this.handleClick.bind(this);
  }
  
  // Handle the click
  async handleClick(query) {
      const delay = ms => new Promise(res => setTimeout(res, ms));
      this.props.update_from_sim();
      await delay(2000)
      this.props.update_from_sim();
      
      // Add the counterfactuals to the queryy
      if (query === "move_factual"){

        this.props.socket.emit('query', 
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
      else if (query === "move_existential"){

        this.props.socket.emit('query', 
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
      else if (query === "stop_factual"){

        this.props.socket.emit('query', 
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
      if (query === "stop_existential"){
        this.props.socket.emit('query', 
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
  
  // Render the information to screen
  render() {

    let run = (this.props.sim_state === 'run')
    let std = (this.props.started === true)
    
    return (
      <div className='Queries' style={{'pointer-events' : (run || !std) ? 'none' : 'auto', 'opacity' : (run || !std) ? '0.5' : '1'}}>
        <div className='QueryHeader'>
          <h2> Query </h2>
          <i style={{ fontWeight: 'normal', 'font-size' : '13px' }}> &emsp; (will use all counterfactual properties specified for all agents)</i>
        </div>
        <div className='Query'>
          <p style={{ 'padding-top': '0.7em', 'padding-right': '2.35em' }}> &#8707;. Might the blue car possibly decide to move?</p>
          <div className='StateButtons'>
            <button className='move_existential' onClick={()=>this.handleClick("move_existential")}>Yes</button>
            &nbsp;&nbsp;
            <button className='stop_factual' onClick={()=>this.handleClick("stop_factual")}>No</button>
          </div>
        </div>
        <div className='Query'>
          <p style={{ 'padding-top': '0.7em', 'padding-right': '0.7em' }}> &#8704;. Would the blue car necessarily decide to move?</p>
          <div className='StateButtons'>
            <button className='move_factual' onClick={()=>this.handleClick("move_factual")}>Yes</button>
            &nbsp;&nbsp;
            <button className='stop_existential' onClick={()=>this.handleClick("stop_existential")}>No</button>
          </div>
        </div>
      </div>
    );
  }
}

export default Queries;

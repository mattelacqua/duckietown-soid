// Import React for components
import React from 'react'
import ReactModal from 'react-modal'

import ModalClose from './ModalClose.js'
import CounterfactualList from './CounterfactualList.js'

class CounterfactualModal extends React.Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

    // Render the conponents
  render() {
    if (!this.props.query_info.querying) return;

    let type = (this.props.query_info.query_type.split('_')[1] === 'existential')
        ? ['Might', 'at least one']
        : ['Would', 'every']
    let move = (this.props.query_info.query_type.split('_')[0] === 'move') ? 'move' : 'stop'

    let stat = 'querying';
    let mark = null;
    let time = Math.floor(((Date.now() / 1000) - this.props.query_info.query_start) / 5) * 5;
    if (this.props.query_info.finished) {
      stat = 'queried';
      mark = (this.props.query_info.result) ? '\u2713' : '\u2717';
      time = (this.props.query_info.resources.time.total.toFixed(3))
    }

    let cfagents = this.props.agents.filter((agent) => agent.counterfactuals.length > 0)

    return (
      <div className="Modal">
        <ReactModal isOpen={this.props.query_info.querying} style={{
                      content : {
                        position: 'absolute',
                        top: '15%',
                        left: '20%',
                        bgcolor: 'background.paper',
                        border: '2px solid #000',
                        boxShadow: 24,
                        height: 'fit-content',
                        width:  '60%',
                      } }} >
          <h3 style={{ fontWeight: 'normal' }}>Question: <i>{type[0]}</i> the agent <b>{move}</b>? In other words, will it do so for <i>{type[1]}</i> possible counterfactual? &nbsp;&nbsp;&nbsp;&nbsp; {mark}</h3>
          <div className="ModalOperate">
            <p style={{ fontSize: '10pt' }}><i>&nbsp;&nbsp;&nbsp;&nbsp; {stat} <b>soid</b>... time elapsed: {time}s</i></p>
            {(this.props.query_info.finished)
             ? <ModalClose agents={this.props.agents}
                           socket={this.props.socket} />
             : null}
          </div>
          {cfagents.map((agent, index) => (
             <div className="ModalAgentCounterfactuals">
               <div class="card" style={{width: '45%'}}>
                 <h4>Agent {index}.</h4>
                 <CounterfactualList agent={agent}
                                     fixed={true}
                                     finished={this.props.query_info.finished}
                                     model={(!this.props.query_info.finished) ? null : this.props.query_info.model}
                                     socket={this.props.socket} />
               </div>
             </div>
          ))}
        </ReactModal>
      </div>
    );
  }
}

export default CounterfactualModal;

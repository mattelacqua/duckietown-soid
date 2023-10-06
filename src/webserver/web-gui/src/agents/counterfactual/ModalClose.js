// Import React for components
import React from 'react'
import '../../environment/StateButtons.css'

class ModalClose extends React.Component {

  constructor(props) {
    super(props);
    this.state = {};
  }

  async handleClick(state) {
    //
  }

  render() {
    return (
      <div class='StateButtons'>
        <button className='clear' onClick={()=>this.handleClick("clear")}>Clear Query</button>
        <button className='alter' onClick={()=>this.handleClick("alter")}>Alter Query</button>
      </div>
    )
  }

}

export default ModalClose;

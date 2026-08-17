import { Component } from 'react'

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <div className="error-icon">!</div>
          <div className="error-title">Application Error</div>
          <div className="error-message">{this.state.error?.message || 'An unexpected error occurred'}</div>
          <button className="error-retry" onClick={() => { this.setState({ hasError: false, error: null }); window.location.reload() }}>
            Reload Application
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

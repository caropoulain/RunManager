import React, {useState} from 'react'
import axios from 'axios'

export default function Upload(){
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)

  async function onSubmit(e){
    e.preventDefault()
    const fd = new FormData()
    fd.append('file', file)
    const res = await axios.post('http://localhost:8000/upload', fd)
    setResult(res.data)
  }

  return (
    <div>
      <form onSubmit={onSubmit}>
        <input type="file" accept=".fit" onChange={e=>setFile(e.target.files[0])}/>
        <button>Envoyer</button>
      </form>
      {result && <pre>{JSON.stringify(result,null,2)}</pre>}
    </div>
  )
}
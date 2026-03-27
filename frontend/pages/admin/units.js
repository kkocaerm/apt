import { useEffect, useState } from "react";
import Layout from "../../components/Layout";
import { api } from "../../lib/api";

export default function UnitsPage() {
  const [units, setUnits] = useState([]);
  const [form, setForm] = useState({ name:"", resident_name:"", resident_email:"" });
  const [message, setMessage] = useState("");

  function load(){ api("/units").then(setUnits).catch(console.error); }
  useEffect(()=>{ load(); },[]);

  async function submit(e){
    e.preventDefault();
    await api("/units", { method:"POST", body:JSON.stringify(form) });
    setForm({ name:"", resident_name:"", resident_email:"" });
    setMessage("Daire eklendi");
    load();
  }

  return (
    <Layout>
      <div className="card">
        <h1>Daireler</h1>
        <form onSubmit={submit}>
          <div className="row">
            <input placeholder="Daire adı" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
            <input placeholder="Sakin adı" value={form.resident_name} onChange={e=>setForm({...form, resident_name:e.target.value})} />
          </div>
          <div style={{height:12}} />
          <input placeholder="Sakin e-postası" value={form.resident_email} onChange={e=>setForm({...form, resident_email:e.target.value})} />
          <div style={{height:12}} />
          <button type="submit">Daire Ekle</button>
        </form>
        {message && <p className="success">{message}</p>}
      </div>
      <div className="card">
        <table><thead><tr><th>Daire</th><th>Sakin</th><th>Borç</th><th>Ödenen</th><th>Kalan</th></tr></thead><tbody>
          {units.map(unit => <tr key={unit.unit_id}><td>{unit.unit_name}</td><td>{unit.resident_name}</td><td>{unit.total_debt} TL</td><td>{unit.total_paid} TL</td><td>{unit.balance} TL</td></tr>)}
        </tbody></table>
      </div>
    </Layout>
  )
}

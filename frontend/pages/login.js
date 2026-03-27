import { useEffect, useState } from "react";
import { api, getToken, setAuth } from "../lib/api";
import { useRouter } from "next/router";

export default function Login() {
  const router = useRouter();
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");
  const [form, setForm] = useState({ tenant_name:"", admin_name:"", admin_email:"", password:"", email:"" });

  useEffect(()=>{ if(getToken()) router.replace("/dashboard"); },[router]);

  async function onSubmit(e){
    e.preventDefault(); setError("");
    try{
      const endpoint=mode==="bootstrap"?"/bootstrap":"/login";
      const payload=mode==="bootstrap"
        ? { tenant_name:form.tenant_name, admin_name:form.admin_name, admin_email:form.admin_email, password:form.password }
        : { email:form.email, password:form.password };
      const data = await api(endpoint, { method:"POST", body:JSON.stringify(payload) });
      setAuth(data); router.push("/dashboard");
    }catch(err){ setError(err.message); }
  }

  return (
    <div className="container" style={{maxWidth:520}}>
      <div className="card">
        <h1>Apartman SaaS</h1>
        <p className="small">İlk kurulum yapılmadıysa önce admin oluştur.</p>
        <div className="nav">
          <button type="button" onClick={()=>setMode("login")}>Giriş</button>
          <button type="button" className="secondary" onClick={()=>setMode("bootstrap")}>İlk Kurulum</button>
        </div>
        <form onSubmit={onSubmit}>
          {mode==="bootstrap" && <>
            <input placeholder="Apartman adı" value={form.tenant_name} onChange={e=>setForm({...form, tenant_name:e.target.value})} />
            <div style={{height:12}} />
            <input placeholder="Yönetici adı" value={form.admin_name} onChange={e=>setForm({...form, admin_name:e.target.value})} />
            <div style={{height:12}} />
            <input placeholder="Yönetici e-postası" value={form.admin_email} onChange={e=>setForm({...form, admin_email:e.target.value})} />
            <div style={{height:12}} />
          </>}
          {mode==="login" && <>
            <input placeholder="E-posta" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
            <div style={{height:12}} />
          </>}
          <input type="password" placeholder="Şifre" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} />
          <div style={{height:12}} />
          <button type="submit">{mode==="bootstrap"?"Kurulumu Tamamla":"Giriş Yap"}</button>
        </form>
        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

import { useRouter } from "next/router";
import { useState } from "react";
import { api, setAuth } from "../lib/api";

export default function AcceptInvite() {
  const router = useRouter();
  const { token } = router.query;
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e){
    e.preventDefault();
    try{
      const data = await api("/invites/accept", { method:"POST", body:JSON.stringify({ token, full_name:fullName, password }) });
      setAuth(data);
      router.push("/dashboard");
    }catch(err){ setError(err.message); }
  }

  return (
    <div className="container" style={{maxWidth:520}}>
      <div className="card">
        <h1>Davet Kabulü</h1>
        <form onSubmit={submit}>
          <input placeholder="Ad Soyad" value={fullName} onChange={e=>setFullName(e.target.value)} />
          <div style={{height:12}} />
          <input type="password" placeholder="Şifre" value={password} onChange={e=>setPassword(e.target.value)} />
          <div style={{height:12}} />
          <button type="submit">Hesabı Oluştur</button>
        </form>
        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

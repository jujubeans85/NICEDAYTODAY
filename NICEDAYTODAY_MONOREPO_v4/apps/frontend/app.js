document.getElementById('playBtn').addEventListener('click',()=>{
  document.getElementById('demo').play().catch(e=>console.log('Blocked:',e));
});
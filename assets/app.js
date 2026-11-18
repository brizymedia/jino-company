(function(){
'use strict';
var d=document;
// 메뉴
var mb=d.querySelector('.mbtn'),sh=d.getElementById('sheet');
if(mb&&sh){mb.addEventListener('click',function(){var on=sh.classList.toggle('on');mb.setAttribute('aria-expanded',on);d.body.style.overflow=on?'hidden':'';});
sh.addEventListener('click',function(e){if(e.target.closest('a')){sh.classList.remove('on');mb.setAttribute('aria-expanded',false);d.body.style.overflow='';}});}
// 등장 — IntersectionObserver 가 안 오는 화면에서도 보이게 스크롤 검사 병행
var rv=[].slice.call(d.querySelectorAll('.rv'));
function chk(){var h=innerHeight;rv=rv.filter(function(el){var r=el.getBoundingClientRect();if(r.top<h*0.94&&r.bottom>0){el.classList.add('in');return false;}return true;});}
chk();addEventListener('scroll',chk,{passive:true});addEventListener('resize',chk);setTimeout(chk,300);
var calm=matchMedia('(prefers-reduced-motion: reduce)').matches;

// ── 대문 출입증: 역할 · 사진이 돌아가며 「체크인」, 마우스를 따라 기울어짐
var pass=d.getElementById('pass');
if(pass){
  var roles=JSON.parse(pass.getAttribute('data-roles')||'[]');
  var imgs=[].slice.call(pass.querySelectorAll('.ph img')),rl=pass.querySelector('.role'),tg=pass.querySelector('.tag'),st=pass.querySelector('.stamp'),i=0;
  function show(n){
    i=n%roles.length;var r=roles[i];
    imgs.forEach(function(im,k){im.classList.toggle('on',k===r.p);});
    rl.innerHTML='<span>'+r.n+'</span>';tg.textContent=r.t;
    if(st){st.style.animation='none';st.offsetWidth;st.style.animation='';}
  }
  show(0);
  if(!calm){
    setInterval(function(){show(i+1);},2600);
    var box=pass.parentNode;
    box.addEventListener('pointermove',function(e){
      if(e.pointerType==='touch')return;
      var b=box.getBoundingClientRect();var x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;
      pass.classList.add('tilt');pass.style.setProperty('--ry',(x*16)+'deg');pass.style.setProperty('--rx',(-y*10)+'deg');
    });
    box.addEventListener('pointerleave',function(){pass.classList.remove('tilt');pass.style.setProperty('--ry','0deg');pass.style.setProperty('--rx','0deg');});
  }
}

// ── 필요한 인력 골라 담기 (대문) → 견적 문의로 넘김
var pk=d.getElementById('picker');
if(pk){
  var cnt=d.getElementById('pickCnt'),lst=d.getElementById('pickList'),go=d.getElementById('pickGo');
  function upd(){
    var on=[].slice.call(pk.querySelectorAll('input:checked'));
    cnt.innerHTML=on.length+'<small>개 선택</small>';
    lst.innerHTML=on.map(function(c){return '<li>'+c.getAttribute('data-n')+'</li>';}).join('')||'<li style="opacity:.6;font-weight:500">아직 고른 인력이 없어요</li>';
    go.href='contact.html?roles='+on.map(function(c){return c.value;}).join(',')+'#form';
  }
  pk.addEventListener('change',upd);upd();
}

// 유튜브: 누르면 그 자리에서 재생 (개인정보 보호 도메인)
d.addEventListener('click',function(e){var b=e.target.closest('[data-yt]');if(!b)return;
var f=d.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-yt')+'?autoplay=1&rel=0';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;f.title='영상 재생';
b.innerHTML='';b.appendChild(f);b.removeAttribute('data-yt');});

// ── 포트폴리오: 분류 거르기 + 사진 크게 보기
var pf=d.getElementById('pf');
if(pf){
  var data=JSON.parse(pf.getAttribute('data-p')||'[]');
  var fb=d.querySelectorAll('.filters button');
  fb.forEach(function(b){b.addEventListener('click',function(){
    fb.forEach(function(x){x.setAttribute('aria-pressed',x===b);});
    var f=b.getAttribute('data-f');
    pf.querySelectorAll('.pj').forEach(function(p){p.hidden=!(f==='all'||p.getAttribute('data-c')===f);});
    history.replaceState(null,'',f==='all'?location.pathname:'#'+f);
  });});
  var h=decodeURIComponent((location.hash||'').slice(1));
  if(h){var t=[].filter.call(fb,function(b){return b.getAttribute('data-f')===h;})[0];if(t)t.click();}
  var lb=d.getElementById('lb'),li=lb.querySelector('img'),lc=lb.querySelector('figcaption'),cur=0,set=[],ev=null,last=null;
  function paint(){var s=set[cur];li.src=s;li.alt=ev.n+' '+(cur+1);lc.innerHTML=ev.n+'<small>'+ev.c+' · '+(cur+1)+' / '+set.length+'</small>';}
  function open(k){last=d.activeElement;ev=data[k];set=ev.i.map(function(c){return 'assets/img/p/'+c+'.webp';});cur=0;paint();lb.classList.add('on');d.body.style.overflow='hidden';lb.querySelector('.x').focus();}
  function close(){lb.classList.remove('on');d.body.style.overflow='';if(last)last.focus();}
  pf.addEventListener('click',function(e){var p=e.target.closest('.pj');if(p)open(+p.getAttribute('data-k'));});
  lb.querySelector('.x').addEventListener('click',close);
  lb.querySelector('.pv').addEventListener('click',function(){cur=(cur+set.length-1)%set.length;paint();});
  lb.querySelector('.nx').addEventListener('click',function(){cur=(cur+1)%set.length;paint();});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  d.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;
    if(e.key==='Escape')close();else if(e.key==='ArrowRight')lb.querySelector('.nx').click();else if(e.key==='ArrowLeft')lb.querySelector('.pv').click();});
}

// 견적 문의 폼
var fm=d.getElementById('form');
if(fm){
  var qs=new URLSearchParams(location.search);
  var q=qs.get('roles');
  if(q){q.split(',').forEach(function(v){var c=fm.querySelector('input[name=roles][value="'+v+'"]');if(c)c.checked=true;});}
  var msg=fm.querySelector('.fmsg');
  function say(t,c){msg.textContent=t;msg.className='fmsg '+(c||'');}
  fm.addEventListener('submit',function(e){
    e.preventDefault();
    if(fm.website.value)return;
    if(!fm.name.value.trim()||!fm.phone.value.trim()){say('성함과 연락처를 적어 주세요.','err');return;}
    if(!/[0-9]{9,}/.test(fm.phone.value.replace(/\D/g,''))){say('연락처를 다시 확인해 주세요.','err');return;}
    if(!fm.agree.checked){say('개인정보 이용 동의에 체크해 주세요.','err');return;}
    var rs=[].map.call(fm.querySelectorAll('input[name=roles]:checked'),function(c){return c.getAttribute('data-n');}).join(', ');
    var text='[지노컴퍼니 인력 견적 문의]\n성함/기관: '+fm.name.value+'\n연락처: '+fm.phone.value+'\n필요한 인력: '+(rs||'-')+'\n행사명: '+(fm.event.value||'-')+'\n날짜: '+(fm.date.value||'미정')+'\n필요 인원: '+(fm.people.value||'-')+'\n장소: '+(fm.place.value||'-')+'\n내용: '+(fm.msg.value||'-');
    var ep=fm.getAttribute('data-endpoint');
    if(ep){
      say('보내는 중입니다…');
      fetch(ep,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify({name:fm.name.value,phone:fm.phone.value,email:'',service:'홈페이지 인력 견적 문의 · '+(rs||'인력'),message:text,page:location.href,website:fm.website.value})})
      .then(function(r){return r.json();}).then(function(j){if(j&&j.ok){say('문의가 접수되었습니다. 곧 연락드리겠습니다.','ok');fm.reset();}else throw 0;})
      .catch(function(){say('전송에 실패했습니다. 전화 '+fm.getAttribute('data-tel')+' 로 연락 주세요.','err');});
    }else{
      // 서버가 연결되기 전: 문자 앱으로 내용을 넘긴다
      say('문자 앱이 열립니다. 내용을 확인하고 보내 주세요.','ok');
      location.href='sms:'+fm.getAttribute('data-tel')+'?body='+encodeURIComponent(text);
    }
  });
}
})();

select qa.id,qa.questionid,qa.questionusageid,q.category,q.name,qa.questionsummary,qa.rightanswer,qa.responsesummary,qa.timemodified,qas.state,qas.fraction,qas.userid, username, from_unixtime(qa.timemodified)
from {question_attempts} qa
join {question} as q
on qa.questionid = q.id
join {question_attempt_steps} as qas
on qas.questionattemptid=qa.id
join {user} as u
on qas.userid=u.id
where qas.state in ('gradedright','gradedwrong')
order by qa.id 

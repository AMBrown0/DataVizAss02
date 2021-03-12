select qz.id,qz.name,qz.grade,qs.questionid,qs.questioncategoryid,qs.slot from {question} qn
join {quiz_slots} AS qs
ON qn.id=qs.questionid
join {quiz} As qz
ON qz.id=qs.quizid

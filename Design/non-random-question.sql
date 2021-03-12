
select * from {question} qn
join {quiz_slots} AS qs
ON qn.id=qs.questionid
where qs.questioncategoryid is NOT NULL

from datetime import datetime
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from smj_chennai.dashboard.serializers import AnalyticsSerializer, DateRangeSerializer
from smj_chennai.core.models import Documents


class PartyBalanceApi(GenericAPIView):
    serializer_class = AnalyticsSerializer

    def get(self, request, *args, **kwargs):
        """get's party balance for the current month"""
        sql = """
                    SELECT 
                    0 as id,
            (c.paid - t.unpaid) AS `value`, 
            p.name AS `key` 
            FROM 
            (
                SELECT 
                SUM(total) as unpaid, 
                party 
                from 
                documents 
                GROUP BY 
                party
            ) t 
            INNER JOIN (
                SELECT 
                SUM(total) as paid, 
                party 
                from 
                charges 
                GROUP BY 
                party
            ) c on c.party = t.party 
            INNER JOIN party p ON p.id = c.party 
            ORDER BY 
            unpaid DESC;
        """

        data = Documents.objects.raw(sql)
        s = self.get_serializer(data, many=True)
        return Response({"status": True, "result": s.data})


class SummaryApi(GenericAPIView):
    serializer_class = AnalyticsSerializer

    def get(self, request, *args, **kwarfs):
        """
        income/expenditure
        """

        request_data = DateRangeSerializer(request.GET).data
        expense_sql = """
                    SELECT  0 as id ,date(docket_date) as `key`,
                    SUM(total) as `value` from documents 
                    WHERE created_at BETWEEN %s AND %s                    
                    GROUP by date(docket_date);
        """

        income_sql = """
            SELECT 0 as id , date(created_at) as `key`, SUM(total) as `value` from charges GROUP by date(created_at);
        """

        expense_data = Documents.objects.raw(
            expense_sql, [request_data["from_date"], request_data["to_date"]]
        )
        e_s = self.get_serializer(expense_data, many=True)

        income_data = Documents.objects.raw(income_sql)
        i_s = self.get_serializer(income_data, many=True)

        result = {
            "expense": e_s.data,
            "income": i_s.data,
        }
        return Response({"status": True, "result": result})

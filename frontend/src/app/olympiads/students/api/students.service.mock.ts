import { Injectable } from '@angular/core'
import { StudentsService } from '@/olympiads/students/api/students.service'
import { AppealMessageReply } from '@/olympiads/students/model/appealMessageReply'
import { CreateAppealInfo } from '@/olympiads/students/model/createAppealInfo'
import { UserResponseStatusHistory } from '@/olympiads/students/model/userResponseStatusHistory'
import { ResponseStatus } from '@/olympiads/students/model/responseStatus'
import { CommonAppealInfo } from '@/olympiads/students/model/commonAppealInfo'
import { HttpEvent, HttpResponse } from '@angular/common/http'
import { UserContestAllAnswer } from '@/olympiads/students/model/userContestAllAnswer'
import { ContestResultSheet } from '@/olympiads/students/model/contestResultSheet'
import { AppealMessage } from '@/olympiads/students/model/appealMessage'
import { Observable } from 'rxjs'
import { UserContestAnswer } from '@/olympiads/students/model/userContestAnswer'


@Injectable( {
    providedIn: 'root'
} )
export class StudentsServiceMock implements StudentsService
{
    canConsumeForm( consumes: string[] ): boolean
    {
        return false
    }

    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: "body", reportProgress?: boolean ): Observable<UserContestAnswer>
    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: any, reportProgress?: boolean ): Observable<UserContestAnswer> | Observable<HttpResponse<UserContestAnswer>> | Observable<HttpEvent<UserContestAnswer>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CommonAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CommonAppealInfo> | Observable<HttpResponse<CommonAppealInfo>> | Observable<HttpEvent<CommonAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CommonAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CommonAppealInfo> | Observable<HttpResponse<CommonAppealInfo>> | Observable<HttpEvent<CommonAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<ContestResultSheet>
    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ContestResultSheet>>
    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ContestResultSheet>>
    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<ContestResultSheet> | Observable<HttpResponse<ContestResultSheet>> | Observable<HttpEvent<ContestResultSheet>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<UserContestAnswer>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<UserContestAnswer> | Observable<HttpResponse<UserContestAnswer>> | Observable<HttpEvent<UserContestAnswer>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<UserContestAnswer>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<UserContestAnswer> | Observable<HttpResponse<UserContestAnswer>> | Observable<HttpEvent<UserContestAnswer>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CommonAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CommonAppealInfo> | Observable<HttpResponse<CommonAppealInfo>> | Observable<HttpEvent<CommonAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CreateAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CreateAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CreateAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CreateAppealInfo> | Observable<HttpResponse<CreateAppealInfo>> | Observable<HttpEvent<CreateAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseStatus>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseStatus>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseStatus>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseStatus> | Observable<HttpResponse<ResponseStatus>> | Observable<HttpEvent<ResponseStatus>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<UserResponseStatusHistory>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserResponseStatusHistory>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserResponseStatusHistory>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<UserResponseStatusHistory> | Observable<HttpResponse<UserResponseStatusHistory>> | Observable<HttpEvent<UserResponseStatusHistory>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CommonAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CommonAppealInfo> | Observable<HttpResponse<CommonAppealInfo>> | Observable<HttpEvent<CommonAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<CreateAppealInfo>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CreateAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CreateAppealInfo>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<CreateAppealInfo> | Observable<HttpResponse<CreateAppealInfo>> | Observable<HttpEvent<CreateAppealInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<UserContestAllAnswer>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserContestAllAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserContestAllAnswer>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<UserContestAllAnswer> | Observable<HttpResponse<UserContestAllAnswer>> | Observable<HttpEvent<UserContestAllAnswer>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<ResponseStatus>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ResponseStatus>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ResponseStatus>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<ResponseStatus> | Observable<HttpResponse<ResponseStatus>> | Observable<HttpEvent<ResponseStatus>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<UserResponseStatusHistory>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserResponseStatusHistory>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserResponseStatusHistory>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<UserResponseStatusHistory> | Observable<HttpResponse<UserResponseStatusHistory>> | Observable<HttpEvent<UserResponseStatusHistory>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

}
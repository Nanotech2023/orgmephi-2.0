import { Observable } from 'rxjs'
import { UserContestAnswer } from '@/olympiads/students/model/userContestAnswer'
import { HttpEvent, HttpResponse } from '@angular/common/http'
import { CommonAppealInfo } from '@/olympiads/students/model/commonAppealInfo'
import { AppealMessageReply } from '@/olympiads/students/model/appealMessageReply'
import { ContestResultSheet } from '@/olympiads/students/model/contestResultSheet'
import { AppealMessage } from '@/olympiads/students/model/appealMessage'
import { CreateAppealInfo } from '@/olympiads/students/model/createAppealInfo'
import { ResponseStatus } from '@/olympiads/students/model/responseStatus'
import { UserResponseStatusHistory } from '@/olympiads/students/model/userResponseStatusHistory'
import { UserContestAllAnswer } from '@/olympiads/students/model/userContestAllAnswer'


export interface StudentsService
{
    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    canConsumeForm( consumes: string[] ): boolean

    /**
     * Get user&#x27;s answer by id
     *
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param answerId Id of the answer
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserContestAnswer>;

    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdAnswerAnswerIdGet( contestId: number, olympiadId: number, stageId: number, answerId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get appeal info
     *
     * @param contestId Id of the contest
     * @param appealId Id of the appeal
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdGet( contestId: number, appealId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Reply appeal for the user&#x27;s response
     *
     * @param body
     * @param contestId Id of the contest
     * @param appealId Id of the appeal
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdAppealAppealIdReplyPost( body: AppealMessageReply, contestId: number, appealId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get the consolidated sheets within a single competition or stage
     *
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<ContestResultSheet>;

    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ContestResultSheet>>;

    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ContestResultSheet>>;

    olympiadOlympiadIdStageStageIdContestContestIdListGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get current user answer for the task
     *
     * @param contestId Id of the contest
     * @param taskId Id of the task
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserContestAnswer>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfGet( contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Add current user answer for the task
     *
     * @param body
     * @param contestId Id of the contest
     * @param taskId Id of the task
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserSelfPost( body: UserContestAnswer, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get user answer for the task
     *
     * @param userId Id of the user
     * @param contestId Id of the contest
     * @param taskId Id of the task
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserContestAnswer>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserContestAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdGet( userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Add user answer for a task
     *
     * @param body
     * @param userId Id of the user
     * @param contestId Id of the contest
     * @param taskId Id of the task
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdTaskTaskIdUserUserIdPost( body: UserContestAnswer, userId: number, contestId: number, taskId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get appeal info for current user&#x27;s response
     *
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create appeal for current user&#x27;s response
     *
     * @param body
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CreateAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CreateAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CreateAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfAppealLastPost( body: AppealMessage, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get user&#x27;s status and mark for reponse
     *
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseStatus>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseStatus>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseStatus>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get status history of current user&#x27;s work
     *
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserResponseStatusHistory>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserResponseStatusHistory>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserResponseStatusHistory>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusHistoryGet( contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set user&#x27;s status and mark for reponse
     * Set user&#x27;s status and mark for reponse, only for inspector
     * @param body
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserSelfStatusPost( body: ResponseStatus, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get appeal info for user&#x27;s response
     *
     * @param contestId Id of the contest
     * @param userId Id of the user
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create appeal for current user&#x27;s response
     *
     * @param body
     * @param contestId Id of the contest
     * @param userId Id of the user
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<CreateAppealInfo>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CreateAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CreateAppealInfo>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdAppealLastPost( body: AppealMessage, contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get all user answers for the contest
     *
     * @param userId Id of the user
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserContestAllAnswer>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserContestAllAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserContestAllAnswer>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdResponseGet( userId: number, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get user&#x27;s status and mark for reponse
     *
     * @param contestId Id of the contest
     * @param userId Id of the user
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<ResponseStatus>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ResponseStatus>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ResponseStatus>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get status history of user&#x27;s work
     *
     * @param contestId Id of the contest
     * @param userId Id of the user
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<UserResponseStatusHistory>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserResponseStatusHistory>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserResponseStatusHistory>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusHistoryGet( contestId: number, userId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set user&#x27;s status and mark for reponse
     * Set user&#x27;s status and mark for reponse, only for inspector
     * @param body
     * @param userId Id of the user
     * @param contestId Id of the contest
     * @param olympiadId Id of the olympiad
     * @param stageId Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadOlympiadIdStageStageIdContestContestIdUserUserIdStatusPost( body: ResponseStatus, userId: number, contestId: number, olympiadId: number, stageId: number, observe: any, reportProgress: boolean ): Observable<any>
}
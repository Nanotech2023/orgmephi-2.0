import { Observable } from 'rxjs'
import { ContestsInStage } from '@/olympiads/tasks/model/contestsInStage'
import { HttpEvent, HttpResponse } from '@angular/common/http'
import { OlympiadCreateBody } from '@/olympiads/tasks/model/olympiadCreateBody'
import { CommonContestId } from '@/olympiads/tasks/model/commonContestId'
import { CommonContestInfo } from '@/olympiads/tasks/model/commonContestInfo'
import { ContestInfoUpdate } from '@/olympiads/tasks/model/contestInfoUpdate'
import { StagesInOlympiad } from '@/olympiads/tasks/model/stagesInOlympiad'
import { CreateStage } from '@/olympiads/tasks/model/createStage'
import { StageInfoId } from '@/olympiads/tasks/model/stageInfoId'
import { CreateContest } from '@/olympiads/tasks/model/createContest'
import { UpdateUserInContest } from '@/olympiads/tasks/model/updateUserInContest'
import { UsersInContest } from '@/olympiads/tasks/model/usersInContest'
import { UserCertificate } from '@/olympiads/tasks/model/userCertificate'
import { VariantsInContest } from '@/olympiads/tasks/model/variantsInContest'
import { CreateVariant } from '@/olympiads/tasks/model/createVariant'
import { VariantInfoId } from '@/olympiads/tasks/model/variantInfoId'
import { TaskCreateBody } from '@/olympiads/tasks/model/taskCreateBody'
import { TaskId } from '@/olympiads/tasks/model/taskId'
import { InlineResponse200 } from '@/olympiads/tasks/model/inlineResponse200'
import { TaskIdTaskBody } from '@/olympiads/tasks/model/taskIdTaskBody'
import { TasksInVariant } from '@/olympiads/tasks/model/tasksInVariant'
import { TaskInVariantImage } from '@/olympiads/tasks/model/taskInVariantImage'
import { VariantInfo } from '@/olympiads/tasks/model/variantInfo'
import { VariantInfoUpdate } from '@/olympiads/tasks/model/variantInfoUpdate'
import { StageInfo } from '@/olympiads/tasks/model/stageInfo'
import { StageInfoUpdate } from '@/olympiads/tasks/model/stageInfoUpdate'
import { AddStatus } from '@/olympiads/tasks/model/addStatus'
import { StatusInfo } from '@/olympiads/tasks/model/statusInfo'
import { AllStatus } from '@/olympiads/tasks/model/allStatus'
import { StatusInfoUpdate } from '@/olympiads/tasks/model/statusInfoUpdate'


export interface TasksService
{
    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    canConsumeForm( consumes: string[] ): boolean

    /**
     * list of olympiads (main contests)
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadAllGet( observe?: 'body', reportProgress?: boolean ): Observable<ContestsInStage>;

    olympiadAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ContestsInStage>>;

    olympiadAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ContestsInStage>>;

    olympiadAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create a new olympiad (main contest)
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadCreatePost( body: OlympiadCreateBody, observe?: 'body', reportProgress?: boolean ): Observable<CommonContestId>;

    olympiadCreatePost( body: OlympiadCreateBody, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonContestId>>;

    olympiadCreatePost( body: OlympiadCreateBody, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonContestId>>;

    olympiadCreatePost( body: OlympiadCreateBody, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get info for the olympiad (main contest)
     *
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadGet( idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonContestInfo>;

    olympiadIdOlympiadGet( idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonContestInfo>>;

    olympiadIdOlympiadGet( idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonContestInfo>>;

    olympiadIdOlympiadGet( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Edit olympiad info
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove olympiad (main contest)
     *
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadRemovePost( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of stages in olympiad
     *
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<StagesInOlympiad>;

    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StagesInOlympiad>>;

    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StagesInOlympiad>>;

    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create a new stage in olympiad
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<StageInfoId>;

    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StageInfoId>>;

    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StageInfoId>>;

    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of contests in stage
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean ): Observable<ContestsInStage>;

    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<ContestsInStage>>;

    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<ContestsInStage>>;

    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create a new contest
     *
     * @param body
     * @param idStage Id of the stage
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonContestId>;

    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonContestId>>;

    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonContestId>>;

    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Add user to contest
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<UpdateUserInContest>;

    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for a contest
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<CommonContestInfo>;

    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<CommonContestInfo>>;

    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<CommonContestInfo>>;

    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Add user to contest
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<UpdateUserInContest>;

    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Edit contest info
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove contest
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove user from contest
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<UpdateUserInContest>;

    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of user in contest
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<UsersInContest>;

    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UsersInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UsersInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * certificate of user in contest
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idUser Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'body', reportProgress?: boolean ): Observable<UserCertificate>;

    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<UserCertificate>>;

    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<UserCertificate>>;

    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of variants in contest
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<VariantsInContest>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<VariantsInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<VariantsInContest>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create a new variant
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean ): Observable<VariantInfoId>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<VariantInfoId>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<VariantInfoId>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove variant
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Create a new task
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'body', reportProgress?: boolean ): Observable<TaskId>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<TaskId>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<TaskId>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get info for a different tasks
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean ): Observable<InlineResponse200>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<InlineResponse200>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<InlineResponse200>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Update task info
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove task
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of tasks in variant
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'body', reportProgress?: boolean ): Observable<TasksInVariant>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<TasksInVariant>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<TasksInVariant>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Task image
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean ): Observable<TaskInVariantImage>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<TaskInVariantImage>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<TaskInVariantImage>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get info for a different variant
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param variantNum Number of the variant in contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'body', reportProgress?: boolean ): Observable<VariantInfo>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<VariantInfo>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<VariantInfo>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Edit variant
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param variantNum Number of the variant in contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get common info for a different stage
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean ): Observable<StageInfo>;

    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StageInfo>>;

    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StageInfo>>;

    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Set stage info for a olympiad
     *
     * @param body
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove stage from olympiad
     *
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * add new user status to library
     *
     * @param body
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userStatusAddPost( body: AddStatus, observe?: 'body', reportProgress?: boolean ): Observable<StatusInfo>;

    userStatusAddPost( body: AddStatus, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StatusInfo>>;

    userStatusAddPost( body: AddStatus, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StatusInfo>>;

    userStatusAddPost( body: AddStatus, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * list of user_status
     *
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userStatusAllGet( observe?: 'body', reportProgress?: boolean ): Observable<AllStatus>;

    userStatusAllGet( observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<AllStatus>>;

    userStatusAllGet( observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<AllStatus>>;

    userStatusAllGet( observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Get info for the user_status
     *
     * @param idStatus Id of the user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userStatusIdStatusGet( idStatus: number, observe?: 'body', reportProgress?: boolean ): Observable<StatusInfo>;

    userStatusIdStatusGet( idStatus: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<StatusInfo>>;

    userStatusIdStatusGet( idStatus: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<StatusInfo>>;

    userStatusIdStatusGet( idStatus: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Edit user_status
     *
     * @param body
     * @param idStatus Id of the user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe: any, reportProgress: boolean ): Observable<any>

    /**
     * Remove user_status
     *
     * @param idStatus Id of the user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    userStatusIdStatusRemovePost( idStatus: number, observe?: 'body', reportProgress?: boolean ): Observable<any>;

    userStatusIdStatusRemovePost( idStatus: number, observe?: 'response', reportProgress?: boolean ): Observable<HttpResponse<any>>;

    userStatusIdStatusRemovePost( idStatus: number, observe?: 'events', reportProgress?: boolean ): Observable<HttpEvent<any>>;

    userStatusIdStatusRemovePost( idStatus: number, observe: any, reportProgress: boolean ): Observable<any>
}
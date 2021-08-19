import { Observable } from 'rxjs'
import {
    AddStatus,
    AllStatus,
    CommonContestId,
    CommonContestInfo,
    ContestInfoUpdate,
    ContestsInStage,
    CreateContest,
    CreateMultipleTask,
    CreatePlainTask,
    CreateRangeTask,
    CreateStage,
    CreateVariant,
    MultipleTaskInfo,
    MultipleTaskInfoUpdate,
    PlainTaskInfo,
    PlainTaskInfoUpdate,
    RangeTaskInfo,
    RangeTaskInfoUpdate,
    StageInfo,
    StageInfoId,
    StageInfoUpdate,
    StagesInOlympiad,
    StatusInfo,
    StatusInfoUpdate,
    TaskId,
    TaskInVariantImage,
    TasksInVariant,
    UpdateUserInContest,
    UserCertificate,
    UsersInContest,
    VariantInfo,
    VariantInfoId,
    VariantInfoUpdate,
    VariantsInContest
} from '@/manage-olympiads/api/models'
import { HttpEvent, HttpResponse } from '@angular/common/http'
import { Configuration } from '@/shared/configuration'


export abstract class OlympiadsService
{
    public configuration = new Configuration()

    protected constructor( configuration: Configuration )
    {
        if ( configuration )
        {
            this.configuration = configuration
        }
        this.configuration.withCredentials = true
    }

    /**
     * list of olympiads (main contests)
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ContestsInStage>;

    abstract olympiadAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ContestsInStage>>;

    abstract olympiadAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ContestsInStage>>;

    abstract olympiadAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get info for the olympiad (main contest)
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadGet( idOlympiad: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<CommonContestInfo>;

    abstract olympiadIdOlympiadGet( idOlympiad: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<CommonContestInfo>>;

    abstract olympiadIdOlympiadGet( idOlympiad: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<CommonContestInfo>>;

    abstract olympiadIdOlympiadGet( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Edit olympiad info
     * @param idOlympiad Id of the olympiad
     * @param contestInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove olympiad (main contest)
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadRemovePost( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of stages in olympiad
     * @param idOlympiad Id of the olympiad
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StagesInOlympiad>;

    abstract olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StagesInOlympiad>>;

    abstract olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StagesInOlympiad>>;

    abstract olympiadIdOlympiadStageAllGet( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Create a new stage in olympiad
     * @param idOlympiad Id of the olympiad
     * @param createStage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StageInfoId>;

    abstract olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StageInfoId>>;

    abstract olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StageInfoId>>;

    abstract olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of contests in stage
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<ContestsInStage>;

    abstract olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<ContestsInStage>>;

    abstract olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<ContestsInStage>>;

    abstract olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Create a new contest
     * @param idStage Id of the stage
     * @param idOlympiad Id of the olympiad
     * @param createContest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<CommonContestId>;

    abstract olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<CommonContestId>>;

    abstract olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<CommonContestId>>;

    abstract olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Add user to contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param updateUserInContest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UpdateUserInContest>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for a contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<CommonContestInfo>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<CommonContestInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<CommonContestInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Add user to contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param updateUserInContest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UpdateUserInContest>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Edit contest info
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param contestInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove user from contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param updateUserInContest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UpdateUserInContest>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UpdateUserInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of user in contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UsersInContest>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UsersInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UsersInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * certificate of user in contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idUser Id of the user
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<UserCertificate>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<UserCertificate>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<UserCertificate>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of variants in contest
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<VariantsInContest>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<VariantsInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<VariantsInContest>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Create a new variant
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param createVariant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<VariantInfoId>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<VariantInfoId>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<VariantInfoId>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove variant
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Create a new task
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param createPlainTaskCreateRangeTaskCreateMultipleTask
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TaskId>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TaskId>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TaskId>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get info for a different tasks
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Update task info
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove task
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of tasks in variant
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TasksInVariant>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TasksInVariant>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TasksInVariant>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Task image
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param idVariant Id of the variant
     * @param idTask Id of the task
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<TaskInVariantImage>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<TaskInVariantImage>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<TaskInVariantImage>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get info for a different variant
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param variantNum Number of the variant in contest
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<VariantInfo>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<VariantInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<VariantInfo>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Edit variant
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param idContest Id of the contest
     * @param variantNum Number of the variant in contest
     * @param variantInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get common info for a different stage
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StageInfo>;

    abstract olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StageInfo>>;

    abstract olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StageInfo>>;

    abstract olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Set stage info for a olympiad
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param stageInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove stage from olympiad
     * @param idOlympiad Id of the olympiad
     * @param idStage Id of the stage
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * add new user status to library
     * @param addStatus
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userStatusAddPost( addStatus: AddStatus, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StatusInfo>;

    abstract userStatusAddPost( addStatus: AddStatus, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StatusInfo>>;

    abstract userStatusAddPost( addStatus: AddStatus, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StatusInfo>>;

    abstract userStatusAddPost( addStatus: AddStatus, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * list of user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userStatusAllGet( observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<AllStatus>;

    abstract userStatusAllGet( observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<AllStatus>>;

    abstract userStatusAllGet( observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<AllStatus>>;

    abstract userStatusAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Get info for the user_status
     * @param idStatus Id of the user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userStatusIdStatusGet( idStatus: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<StatusInfo>;

    abstract userStatusIdStatusGet( idStatus: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<StatusInfo>>;

    abstract userStatusIdStatusGet( idStatus: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<StatusInfo>>;

    abstract userStatusIdStatusGet( idStatus: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Edit user_status
     * @param idStatus Id of the user_status
     * @param statusInfoUpdate
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>

    /**
     * Remove user_status
     * @param idStatus Id of the user_status
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    abstract userStatusIdStatusRemovePost( idStatus: number, observe?: 'body', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>;

    abstract userStatusIdStatusRemovePost( idStatus: number, observe?: 'response', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpResponse<any>>;

    abstract userStatusIdStatusRemovePost( idStatus: number, observe?: 'events', reportProgress?: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<HttpEvent<any>>;

    abstract userStatusIdStatusRemovePost( idStatus: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: 'application/json' } ): Observable<any>
}
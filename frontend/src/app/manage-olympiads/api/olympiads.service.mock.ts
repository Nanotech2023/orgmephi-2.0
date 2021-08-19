import { OlympiadsService } from '@/manage-olympiads/api/olympiads.service'
import {
    AddStatus,
    AllStatus,
    CommonContestId,
    CommonContestInfo,
    ContestInfoUpdate,
    ContestsInStage,
    ContestsInStageContestsList,
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
import { Observable, of } from 'rxjs'
import { Injectable } from '@angular/core'
import { Configuration } from '@/shared/configuration'


@Injectable()
export class OlympiadsServiceMock extends OlympiadsService
{
    constructor()
    {
        super( new Configuration() )
    }

    olympiadAllGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ContestsInStage>
    olympiadAllGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ContestsInStage>>
    olympiadAllGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ContestsInStage>>
    olympiadAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadAllGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ContestsInStage> | Observable<HttpResponse<ContestsInStage>> | Observable<HttpEvent<ContestsInStage>> | Observable<any>
    {
        const olympiads: Array<ContestsInStageContestsList> = [
            {
                contest_id: 401,
                description: "Курчатов Математика",
                rules: "3 задания, 4 часа",
                visibility: true,
                laureate_condition: "Количество баллов >=7",
                winning_condition: "Количество баллов >=9",
                start_time: "19 октября 2021",
                end_time: "20 октября 2021"
            },
            {
                contest_id: 402,
                description: "Курчатов Физика",
                rules: "3 задания, 4 часа",
                visibility: true,
                laureate_condition: "Количество баллов >=7",
                winning_condition: "Количество баллов >=9",
                start_time: "23 октября 2021",
                end_time: "24 октября 2021"
            },
            {
                contest_id: 403,
                description: "РосАтом Математика",
                rules: "3 задания, 3 часа",
                visibility: true,
                laureate_condition: "Количество баллов >=7",
                winning_condition: "Количество баллов >=9",
                start_time: "10 февраля 2022",
                end_time: "10 февраля 2022"
            },
            {
                contest_id: 404,
                description: "РосАтом Физика",
                rules: "3 задания, 3 часа",
                visibility: true,
                laureate_condition: "Количество баллов >=7",
                winning_condition: "Количество баллов >=9",
                start_time: "17 февраля 2022",
                end_time: "17 февраля 2022"
            }
        ]
        return of( { contests_list: olympiads } )
    }

    olympiadIdOlympiadGet( idOlympiad: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestInfo>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<CommonContestInfo>>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<CommonContestInfo>>
    olympiadIdOlympiadGet( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestInfo> | Observable<HttpResponse<CommonContestInfo>> | Observable<HttpEvent<CommonContestInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadPatch( idOlympiad: number, contestInfoUpdate: ContestInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StagesInOlympiad>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<StagesInOlympiad>>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<StagesInOlympiad>>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StagesInOlympiad> | Observable<HttpResponse<StagesInOlympiad>> | Observable<HttpEvent<StagesInOlympiad>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StageInfoId>
    olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<StageInfoId>>
    olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<StageInfoId>>
    olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageCreatePost( idOlympiad: number, createStage: CreateStage, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StageInfoId> | Observable<HttpResponse<StageInfoId>> | Observable<HttpEvent<StageInfoId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ContestsInStage>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<ContestsInStage>>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<ContestsInStage>>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<ContestsInStage> | Observable<HttpResponse<ContestsInStage>> | Observable<HttpEvent<ContestsInStage>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestId>
    olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<CommonContestId>>
    olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<CommonContestId>>
    olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestCreatePost( idStage: number, idOlympiad: number, createContest: CreateContest, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestId> | Observable<HttpResponse<CommonContestId>> | Observable<HttpEvent<CommonContestId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestInfo>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<CommonContestInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<CommonContestInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<CommonContestInfo> | Observable<HttpResponse<CommonContestInfo>> | Observable<HttpEvent<CommonContestInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( idOlympiad: number, idStage: number, idContest: number, contestInfoUpdate: ContestInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( idOlympiad: number, idStage: number, idContest: number, updateUserInContest: UpdateUserInContest, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UsersInContest>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<UsersInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<UsersInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UsersInContest> | Observable<HttpResponse<UsersInContest>> | Observable<HttpEvent<UsersInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UserCertificate>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<UserCertificate>>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<UserCertificate>>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<UserCertificate> | Observable<HttpResponse<UserCertificate>> | Observable<HttpEvent<UserCertificate>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantsInContest>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<VariantsInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<VariantsInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantsInContest> | Observable<HttpResponse<VariantsInContest>> | Observable<HttpEvent<VariantsInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantInfoId>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<VariantInfoId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<VariantInfoId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( idOlympiad: number, idStage: number, idContest: number, createVariant: CreateVariant, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantInfoId> | Observable<HttpResponse<VariantInfoId>> | Observable<HttpEvent<VariantInfoId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TaskId>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TaskId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TaskId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, createPlainTaskCreateRangeTaskCreateMultipleTask: CreatePlainTask | CreateRangeTask | CreateMultipleTask, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TaskId> | Observable<HttpResponse<TaskId>> | Observable<HttpEvent<TaskId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo> | Observable<HttpResponse<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>> | Observable<HttpEvent<PlainTaskInfo | RangeTaskInfo | MultipleTaskInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, plainTaskInfoUpdateRangeTaskInfoUpdateMultipleTaskInfoUpdate: PlainTaskInfoUpdate | RangeTaskInfoUpdate | MultipleTaskInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TasksInVariant>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TasksInVariant>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TasksInVariant>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TasksInVariant> | Observable<HttpResponse<TasksInVariant>> | Observable<HttpEvent<TasksInVariant>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TaskInVariantImage>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<TaskInVariantImage>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<TaskInVariantImage>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<TaskInVariantImage> | Observable<HttpResponse<TaskInVariantImage>> | Observable<HttpEvent<TaskInVariantImage>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantInfo>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<VariantInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<VariantInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<VariantInfo> | Observable<HttpResponse<VariantInfo>> | Observable<HttpEvent<VariantInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( idOlympiad: number, idStage: number, idContest: number, variantNum: number, variantInfoUpdate: VariantInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StageInfo>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<StageInfo>>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<StageInfo>>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StageInfo> | Observable<HttpResponse<StageInfo>> | Observable<HttpEvent<StageInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStagePatch( idOlympiad: number, idStage: number, stageInfoUpdate: StageInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userStatusAddPost( addStatus: AddStatus, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StatusInfo>
    userStatusAddPost( addStatus: AddStatus, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<StatusInfo>>
    userStatusAddPost( addStatus: AddStatus, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<StatusInfo>>
    userStatusAddPost( addStatus: AddStatus, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusAddPost( addStatus: AddStatus, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StatusInfo> | Observable<HttpResponse<StatusInfo>> | Observable<HttpEvent<StatusInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusAllGet( observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<AllStatus>
    userStatusAllGet( observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<AllStatus>>
    userStatusAllGet( observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<AllStatus>>
    userStatusAllGet( observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusAllGet( observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<AllStatus> | Observable<HttpResponse<AllStatus>> | Observable<HttpEvent<AllStatus>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusGet( idStatus: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StatusInfo>
    userStatusIdStatusGet( idStatus: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<StatusInfo>>
    userStatusIdStatusGet( idStatus: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<StatusInfo>>
    userStatusIdStatusGet( idStatus: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusIdStatusGet( idStatus: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<StatusInfo> | Observable<HttpResponse<StatusInfo>> | Observable<HttpEvent<StatusInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusIdStatusPatch( idStatus: number, statusInfoUpdate: StatusInfoUpdate, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusRemovePost( idStatus: number, observe?: "body", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusIdStatusRemovePost( idStatus: number, observe?: "response", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpResponse<any>>
    userStatusIdStatusRemovePost( idStatus: number, observe?: "events", reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<HttpEvent<any>>
    userStatusIdStatusRemovePost( idStatus: number, observe: any, reportProgress: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any>
    userStatusIdStatusRemovePost( idStatus: number, observe?: any, reportProgress?: boolean, options?: { httpHeaderAccept?: "application/json" } ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }
}
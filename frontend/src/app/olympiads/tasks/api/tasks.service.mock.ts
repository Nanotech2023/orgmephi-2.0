import { Injectable } from '@angular/core'
import { TasksService } from '@/olympiads/tasks/api/tasks.service'
import { VariantInfo } from '@/olympiads/tasks/model/variantInfo'
import { TaskId } from '@/olympiads/tasks/model/taskId'
import { StageInfo } from '@/olympiads/tasks/model/stageInfo'
import { UsersInContest } from '@/olympiads/tasks/model/usersInContest'
import { InlineResponse200 } from '@/olympiads/tasks/model/inlineResponse200'
import { ContestInfoUpdate } from '@/olympiads/tasks/model/contestInfoUpdate'
import { StageInfoUpdate } from '@/olympiads/tasks/model/stageInfoUpdate'
import { OlympiadCreateBody } from '@/olympiads/tasks/model/olympiadCreateBody'
import { CreateStage } from '@/olympiads/tasks/model/createStage'
import { UpdateUserInContest } from '@/olympiads/tasks/model/updateUserInContest'
import { TaskIdTaskBody } from '@/olympiads/tasks/model/taskIdTaskBody'
import { StatusInfoUpdate } from '@/olympiads/tasks/model/statusInfoUpdate'
import { AllStatus } from '@/olympiads/tasks/model/allStatus'
import { AddStatus } from '@/olympiads/tasks/model/addStatus'
import { CreateContest } from '@/olympiads/tasks/model/createContest'
import { TaskInVariantImage } from '@/olympiads/tasks/model/taskInVariantImage'
import { CommonContestId } from '@/olympiads/tasks/model/commonContestId'
import { HttpEvent, HttpResponse } from '@angular/common/http'
import { CreateVariant } from '@/olympiads/tasks/model/createVariant'
import { Observable, of } from 'rxjs'
import { VariantsInContest } from '@/olympiads/tasks/model/variantsInContest'
import { ContestsInStage } from '@/olympiads/tasks/model/contestsInStage'
import { VariantInfoId } from '@/olympiads/tasks/model/variantInfoId'
import { StatusInfo } from '@/olympiads/tasks/model/statusInfo'
import { TaskCreateBody } from '@/olympiads/tasks/model/taskCreateBody'
import { StagesInOlympiad } from '@/olympiads/tasks/model/stagesInOlympiad'
import { CommonContestInfo } from '@/olympiads/tasks/model/commonContestInfo'
import { TasksInVariant } from '@/olympiads/tasks/model/tasksInVariant'
import { VariantInfoUpdate } from '@/olympiads/tasks/model/variantInfoUpdate'
import { UserCertificate } from '@/olympiads/tasks/model/userCertificate'
import { StageInfoId } from '@/olympiads/tasks/model/stageInfoId'


@Injectable( {
    providedIn: 'root'
} )
export class TasksServiceMock implements TasksService
{
    canConsumeForm( consumes: string[] ): boolean
    {
        return false
    }

    olympiadAllGet( observe?: "body", reportProgress?: boolean ): Observable<ContestsInStage>
    olympiadAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ContestsInStage>>
    olympiadAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ContestsInStage>>
    olympiadAllGet( observe: any, reportProgress: boolean ): Observable<any>
    olympiadAllGet( observe?: any, reportProgress?: boolean ): Observable<ContestsInStage> | Observable<HttpResponse<ContestsInStage>> | Observable<HttpEvent<ContestsInStage>> | Observable<any>
    {
        return of( {
            contestsList: [
                {
                    contestId: 123,
                    description: 'test description',
                    startTime: new Date(),
                    endTime: new Date(),
                    laureateCondition: 'test laureateCondition',
                    visibility: true
                }, {
                    contestId: 1234,
                    description: 'test description 2',
                    startTime: new Date(),
                    endTime: new Date( 2022, 1, 1 ),
                    laureateCondition: 'test laureateCondition 2',
                    visibility: true
                }
            ]
        } )
    }

    olympiadCreatePost( body: OlympiadCreateBody, observe?: "body", reportProgress?: boolean ): Observable<CommonContestId>
    olympiadCreatePost( body: OlympiadCreateBody, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonContestId>>
    olympiadCreatePost( body: OlympiadCreateBody, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonContestId>>
    olympiadCreatePost( body: OlympiadCreateBody, observe: any, reportProgress: boolean ): Observable<any>
    olympiadCreatePost( body: OlympiadCreateBody, observe?: any, reportProgress?: boolean ): Observable<CommonContestId> | Observable<HttpResponse<CommonContestId>> | Observable<HttpEvent<CommonContestId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadGet( idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<CommonContestInfo>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonContestInfo>>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonContestInfo>>
    olympiadIdOlympiadGet( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadGet( idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<CommonContestInfo> | Observable<HttpResponse<CommonContestInfo>> | Observable<HttpEvent<CommonContestInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadPatch( body: ContestInfoUpdate, idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadRemovePost( idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<StagesInOlympiad>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StagesInOlympiad>>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StagesInOlympiad>>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageAllGet( idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<StagesInOlympiad> | Observable<HttpResponse<StagesInOlympiad>> | Observable<HttpEvent<StagesInOlympiad>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<StageInfoId>
    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StageInfoId>>
    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StageInfoId>>
    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageCreatePost( body: CreateStage, idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<StageInfoId> | Observable<HttpResponse<StageInfoId>> | Observable<HttpEvent<StageInfoId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean ): Observable<ContestsInStage>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<ContestsInStage>>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<ContestsInStage>>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestAllGet( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean ): Observable<ContestsInStage> | Observable<HttpResponse<ContestsInStage>> | Observable<HttpEvent<ContestsInStage>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: "body", reportProgress?: boolean ): Observable<CommonContestId>
    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonContestId>>
    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonContestId>>
    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestCreatePost( body: CreateContest, idStage: number, idOlympiad: number, observe?: any, reportProgress?: boolean ): Observable<CommonContestId> | Observable<HttpResponse<CommonContestId>> | Observable<HttpEvent<CommonContestId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestAdduserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<CommonContestInfo>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<CommonContestInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<CommonContestInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<CommonContestInfo> | Observable<HttpResponse<CommonContestInfo>> | Observable<HttpEvent<CommonContestInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestMoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestPatch( body: ContestInfoUpdate, idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemovePost( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<UpdateUserInContest>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UpdateUserInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestRemoveuserPost( body: UpdateUserInContest, idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<UpdateUserInContest> | Observable<HttpResponse<UpdateUserInContest>> | Observable<HttpEvent<UpdateUserInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<UsersInContest>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UsersInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UsersInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestUserAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<UsersInContest> | Observable<HttpResponse<UsersInContest>> | Observable<HttpEvent<UsersInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "body", reportProgress?: boolean ): Observable<UserCertificate>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<UserCertificate>>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<UserCertificate>>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestUserIdUserCertificateGet( idOlympiad: number, idStage: number, idContest: number, idUser: number, observe?: any, reportProgress?: boolean ): Observable<UserCertificate> | Observable<HttpResponse<UserCertificate>> | Observable<HttpEvent<UserCertificate>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<VariantsInContest>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<VariantsInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<VariantsInContest>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantAllGet( idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<VariantsInContest> | Observable<HttpResponse<VariantsInContest>> | Observable<HttpEvent<VariantsInContest>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: "body", reportProgress?: boolean ): Observable<VariantInfoId>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<VariantInfoId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<VariantInfoId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantCreatePost( body: CreateVariant, idOlympiad: number, idStage: number, idContest: number, observe?: any, reportProgress?: boolean ): Observable<VariantInfoId> | Observable<HttpResponse<VariantInfoId>> | Observable<HttpEvent<VariantInfoId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "body", reportProgress?: boolean ): Observable<TaskId>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<TaskId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<TaskId>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskCreatePost( body: TaskCreateBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: any, reportProgress?: boolean ): Observable<TaskId> | Observable<HttpResponse<TaskId>> | Observable<HttpEvent<TaskId>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean ): Observable<InlineResponse200>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<InlineResponse200>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<InlineResponse200>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean ): Observable<InlineResponse200> | Observable<HttpResponse<InlineResponse200>> | Observable<HttpEvent<InlineResponse200>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskPatch( body: TaskIdTaskBody, idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTaskIdTaskRemovePost( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "body", reportProgress?: boolean ): Observable<TasksInVariant>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<TasksInVariant>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<TasksInVariant>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksAllGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, observe?: any, reportProgress?: boolean ): Observable<TasksInVariant> | Observable<HttpResponse<TasksInVariant>> | Observable<HttpEvent<TasksInVariant>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "body", reportProgress?: boolean ): Observable<TaskInVariantImage>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<TaskInVariantImage>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<TaskInVariantImage>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantIdVariantTasksIdTaskTaskimageGet( idOlympiad: number, idStage: number, idContest: number, idVariant: number, idTask: number, observe?: any, reportProgress?: boolean ): Observable<TaskInVariantImage> | Observable<HttpResponse<TaskInVariantImage>> | Observable<HttpEvent<TaskInVariantImage>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "body", reportProgress?: boolean ): Observable<VariantInfo>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<VariantInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<VariantInfo>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumGet( idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: any, reportProgress?: boolean ): Observable<VariantInfo> | Observable<HttpResponse<VariantInfo>> | Observable<HttpEvent<VariantInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageContestIdContestVariantVariantNumPatch( body: VariantInfoUpdate, idOlympiad: number, idStage: number, idContest: number, variantNum: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean ): Observable<StageInfo>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StageInfo>>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StageInfo>>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageGet( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean ): Observable<StageInfo> | Observable<HttpResponse<StageInfo>> | Observable<HttpEvent<StageInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStagePatch( body: StageInfoUpdate, idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe: any, reportProgress: boolean ): Observable<any>
    olympiadIdOlympiadStageIdStageRemovePost( idOlympiad: number, idStage: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userStatusAddPost( body: AddStatus, observe?: "body", reportProgress?: boolean ): Observable<StatusInfo>
    userStatusAddPost( body: AddStatus, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StatusInfo>>
    userStatusAddPost( body: AddStatus, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StatusInfo>>
    userStatusAddPost( body: AddStatus, observe: any, reportProgress: boolean ): Observable<any>
    userStatusAddPost( body: AddStatus, observe?: any, reportProgress?: boolean ): Observable<StatusInfo> | Observable<HttpResponse<StatusInfo>> | Observable<HttpEvent<StatusInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusAllGet( observe?: "body", reportProgress?: boolean ): Observable<AllStatus>
    userStatusAllGet( observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<AllStatus>>
    userStatusAllGet( observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<AllStatus>>
    userStatusAllGet( observe: any, reportProgress: boolean ): Observable<any>
    userStatusAllGet( observe?: any, reportProgress?: boolean ): Observable<AllStatus> | Observable<HttpResponse<AllStatus>> | Observable<HttpEvent<AllStatus>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusGet( idStatus: number, observe?: "body", reportProgress?: boolean ): Observable<StatusInfo>
    userStatusIdStatusGet( idStatus: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<StatusInfo>>
    userStatusIdStatusGet( idStatus: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<StatusInfo>>
    userStatusIdStatusGet( idStatus: number, observe: any, reportProgress: boolean ): Observable<any>
    userStatusIdStatusGet( idStatus: number, observe?: any, reportProgress?: boolean ): Observable<StatusInfo> | Observable<HttpResponse<StatusInfo>> | Observable<HttpEvent<StatusInfo>> | Observable<any>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe: any, reportProgress: boolean ): Observable<any>
    userStatusIdStatusPatch( body: StatusInfoUpdate, idStatus: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }

    userStatusIdStatusRemovePost( idStatus: number, observe?: "body", reportProgress?: boolean ): Observable<any>
    userStatusIdStatusRemovePost( idStatus: number, observe?: "response", reportProgress?: boolean ): Observable<HttpResponse<any>>
    userStatusIdStatusRemovePost( idStatus: number, observe?: "events", reportProgress?: boolean ): Observable<HttpEvent<any>>
    userStatusIdStatusRemovePost( idStatus: number, observe: any, reportProgress: boolean ): Observable<any>
    userStatusIdStatusRemovePost( idStatus: number, observe?: any, reportProgress?: boolean ): Observable<any> | Observable<HttpResponse<any>> | Observable<HttpEvent<any>>
    {
        throw new Error( 'not implemented' )
    }
}
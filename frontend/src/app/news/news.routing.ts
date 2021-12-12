import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { NewsListComponent } from '@/news/containers/news-list/news-list.component'
import { NewsListItemComponent } from '@/news/components/news-list-item/news-list-item.component'


export const COMPONENTS = [
    NewsListComponent,
    NewsListItemComponent
]

const routes: Routes =
    [
        {
            path: 'news', component: NewsListComponent
        },
    ]


@NgModule( {
    imports: [ RouterModule.forChild( routes ) ],
    exports: [ RouterModule ]
} )
export class NewsRoutingModule {}